"""Tab 4 — Cảnh báo break out thất bại (SEPA): xem backend/screening/sepa_failed_breakout/."""
import streamlit as st

from backend import scan_failed_breakout, FAILED_BREAKOUT_SIGNALS
from database import db_stats

from .top_rank import cached_universe


@st.cache_data(ttl=6 * 3600, show_spinner=False)
def cached_failed_breakout(symbols: tuple, check_liquidity: bool, db_sig: tuple):
    return scan_failed_breakout(list(symbols), check_liquidity=check_liquidity)


def render():
    st.markdown('<div class="section-title">⚠️ Cảnh báo break out thất bại (SEPA)</div>', unsafe_allow_html=True)
    st.caption("Đóng cửa dưới MA20 · 3 đáy thấp hơn · tăng giá KL thấp, giảm giá KL cao. "
               "Xem xét theo cụm tín hiệu — càng nhiều tín hiệu cùng lúc càng nên cân nhắc cắt lỗ sớm. "
               "Ngưỡng sửa ở backend/screening/sepa_failed_breakout/config.py")

    n_sym, n_rows, db_last = db_stats()
    if n_sym == 0:
        st.warning("DB chưa có dữ liệu. Chạy `python DB.py import` rồi `python DB.py update`, sau đó tải lại trang.")
        return
    db_sig = (n_sym, n_rows, db_last)

    holdings_raw = st.text_input("Mã đang nắm giữ (cách nhau bằng dấu phẩy, để trống = quét cả thị trường)",
                                 key="exit_holdings", placeholder="VD: HPG, FPT, SSI")
    holdings = tuple(dict.fromkeys(c.strip().upper() for c in holdings_raw.replace(";", ",").split(",") if c.strip()))

    if holdings:
        symbols, check_liq = holdings, False
    else:
        c1, c2 = st.columns(2)
        with c1:
            opts = {"Thanh khoản ≥ 1 tỷ/phiên": (0, 1.0), "Top 100 thanh khoản": (100, 1.0)}
            size, min_val = opts[st.selectbox("Phạm vi quét", list(opts), key="exit_uni")]
        with c2:
            min_sig = st.slider("Số tín hiệu tối thiểu", 0, len(FAILED_BREAKOUT_SIGNALS), 2, key="exit_min")
        universe, _ = cached_universe(size, min_val, db_sig)
        symbols, check_liq = tuple(universe), True

    with st.spinner(f"Đang kiểm tra {len(symbols)} mã..."):
        df, failed = cached_failed_breakout(symbols, check_liq, db_sig)
    if df.empty:
        st.info("Không có mã nào để kiểm tra.")
        if failed:
            st.caption(", ".join(failed))
        return

    shown = df if holdings else df[df["Số tín hiệu"] >= min_sig]
    st.markdown(f"**{len(shown)}** / {len(df)} mã" + ("" if holdings else f" có ≥ {min_sig} tín hiệu")
                + f"  ·  phiên mới nhất {df['Ngày'].max()}")

    names = [n for n, _ in FAILED_BREAKOUT_SIGNALS]
    view = shown[["Mã", "Sàn", "Giá", "Số tín hiệu", "Mức cảnh báo"] + names].copy()
    for n in names:
        view[n] = view[n].map({True: "⚠", False: "–"})
    st.dataframe(view, use_container_width=True, hide_index=True)

    if st.checkbox("Xem chi tiết giá trị từng tín hiệu", key="exit_detail"):
        det = shown[["Mã"] + [n + " | chi tiết" for n in names]].copy()
        det.columns = ["Mã"] + names
        st.dataframe(det, use_container_width=True, hide_index=True)

    if failed:
        with st.expander(f"{len(failed)} mã bị bỏ qua"):
            st.caption(", ".join(failed))
