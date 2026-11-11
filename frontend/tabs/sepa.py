"""Tab 3 — Bộ lọc kỹ thuật SEPA (7 điều kiện, xem backend/screening/sepa/)."""
import pandas as pd
import streamlit as st

from backend import scan_sepa, SEPA_CRITERIA
from database import db_stats

from .top_rank import cached_universe


@st.cache_data(ttl=6 * 3600, show_spinner=False)
def cached_sepa(symbols: tuple, db_sig: tuple):
    # db_sig đổi (DB có giá mới) -> cache tự làm mới
    return scan_sepa(list(symbols))


def render():
    st.markdown('<div class="section-title">🔎 Bộ lọc kỹ thuật SEPA</div>', unsafe_allow_html=True)
    st.caption("Giá > MA50 > MA150 > MA200 · MA200 hướng lên · đỉnh/đáy cao dần · "
               "dòng tiền (tuần & ngày) · cách đáy 52W ≥ 30% · cách đỉnh 52W ≤ 25%. "
               "Ngưỡng sửa ở backend/screening/sepa/config.py")

    n_sym, n_rows, db_last = db_stats()
    if n_sym == 0:
        st.warning("DB chưa có dữ liệu. Chạy `python DB.py import` rồi `python DB.py update`, sau đó tải lại trang.")
        return

    c1, c2 = st.columns(2)
    with c1:
        opts = {"Thanh khoản ≥ 1 tỷ/phiên": (0, 1.0), "Top 100 thanh khoản": (100, 1.0), "Toàn bộ mã": (0, 0.0)}
        choice = st.selectbox("Phạm vi quét", list(opts), key="sepa_uni")
    with c2:
        min_ok = st.slider("Số điều kiện tối thiểu", 1, len(SEPA_CRITERIA), len(SEPA_CRITERIA), key="sepa_min")

    size, min_val = opts[choice]
    db_sig = (n_sym, n_rows, db_last)
    symbols, _ = cached_universe(size, min_val, db_sig)
    with st.spinner(f"Đang lọc {len(symbols)} mã..."):
        df, failed = cached_sepa(tuple(symbols), db_sig)

    if df.empty:
        st.info("Không có mã nào để lọc.")
        return

    shown = df[df["Số ĐK đạt"] >= min_ok]
    st.markdown(f"**{len(shown)}** / {len(df)} mã đạt ≥ {min_ok} điều kiện"
                f"  ·  phiên mới nhất {df['Ngày'].max()}")

    names = [n for n, _ in SEPA_CRITERIA]
    view = shown[["Mã", "Sàn", "Giá", "Số ĐK đạt"] + names].copy()
    for n in names:
        view[n] = view[n].map({True: "✓", False: "✗"})
    st.dataframe(view, use_container_width=True, hide_index=True)

    if st.checkbox("Xem chi tiết giá trị từng điều kiện", key="sepa_detail"):
        det = shown[["Mã"] + [n + " | chi tiết" for n in names]].copy()
        det.columns = ["Mã"] + names
        st.dataframe(det, use_container_width=True, hide_index=True)

    if failed:
        with st.expander(f"{len(failed)} mã bị bỏ qua"):
            st.caption(", ".join(failed))
