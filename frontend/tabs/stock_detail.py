"""Tab 2 — Phân tích 1 mã: nhập mã -> lấy giá -> dự đoán -> hiển thị từng khối (frontend/sections/)."""
import pandas as pd
import streamlit as st

from backend import to_daily_indexed, predict_trend
from database import db_meta, fetch_live

from ..sections import (
    summary_card, probability, price_chart, euphoria_panel,
    regime_panel, feature_table, disclaimer,
)


def render():
    st.markdown('<div class="section-title">🔎 Nhập mã bất kỳ — tự dò sàn & phân tích xu hướng</div>', unsafe_allow_html=True)
    d1, d2 = st.columns([1.4, 1])
    with d1:
        code_in = st.text_input("Mã cổ phiếu", value=st.session_state.get("selected_ticker", "HPG"),
                                placeholder="VD: HPG, ANV, SHS, BSR...").upper().strip()
    with d2:
        st.markdown("<div style='padding-top:28px;'></div>", unsafe_allow_html=True)
        run = st.button("🔍 Chạy phân tích xu hướng", width="stretch", type="primary")

    code = (code_in or "HPG").split()[0].upper()
    st.session_state["selected_ticker"] = code

    in_db = db_meta(code)[1] > 0
    refresh_tv = st.checkbox("🔄 Lấy thêm giá mới từ TradingView", value=False, key="refresh_one",
                             help="Mặc định đọc từ DB. Tick để kéo các phiên còn thiếu rồi lưu vào DB.") if in_db else False
    with st.spinner(f"Đang đọc dữ liệu {code} từ DB..." if (in_db and not refresh_tv)
                    else f"Đang lấy dữ liệu {code} từ TradingView..."):
        # ưu tiên DB; chỉ gọi TradingView khi mã chưa có trong DB hoặc người dùng tick cập nhật
        df_raw, selected_exchange = fetch_live(code, n_bars=2000, offline=(in_db and not refresh_tv))
    if df_raw is not None and not df_raw.empty:
        st.caption(f"🗄️ Nguồn: {'DB' if (in_db and not refresh_tv) else 'TradingView → DB'} · "
                   f"phiên mới nhất {pd.to_datetime(df_raw['datetime']).max():%d/%m/%Y}" if 'datetime' in df_raw.columns
                   else "🗄️ Nguồn: TradingView")

    if df_raw is None or df_raw.empty:
        st.warning(
            f"Mã cổ phiếu **{code}** không tồn tại trên HOSE, HNX hoặc UPCOM.\n\n"
            "Ví dụ hợp lệ: HPG, FPT, SHS, PVS, BSR, ACV..."
        )
        st.stop()

    df_daily = to_daily_indexed(df_raw)
    try:
        r = predict_trend(df_daily)
    except Exception as e:
        st.error(f"Không tính được xu hướng cho {code}: {e}")
        st.stop()

    price = float(df_daily["close"].iloc[-1])
    prev = float(df_daily["close"].iloc[-2]) if len(df_daily) > 1 else price
    chg = (price / prev - 1) * 100 if prev else 0.0

    summary_card.render(code, selected_exchange, price, chg, r, df_daily)
    probability.render(r)
    price_chart.render(df_daily)
    euphoria_panel.render(code, df_daily)

    left, right = st.columns([1.05, 1])
    with left:
        regime_panel.render(r)
    with right:
        feature_table.render(r)

    disclaimer.render(r)
