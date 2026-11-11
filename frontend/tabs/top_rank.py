"""Tab 1 — Top mã có xác suất tăng cao nhất."""
import pandas as pd
import streamlit as st

from backend import load_universe, scan_universe
from database import db_stats

from ..styles import TOP_TABLE_CSS

TOP_SHOW = 20


@st.cache_data(ttl=3600, show_spinner=False)
def cached_universe(size: int, min_val: float, db_sig: tuple):
    return load_universe(size, min_val)

@st.cache_data(ttl=6 * 3600, show_spinner=False)
def cached_rank(symbols: tuple, db_sig: tuple):
    # db_sig = (số mã, số dòng, ngày mới nhất) của DB -> DB đổi thì cache tự làm mới
    return scan_universe(list(symbols))

def render():
    st.markdown('<div class="section-title">🏆 Top mã có xác suất tăng cao nhất</div>', unsafe_allow_html=True)
    UNI_OPTS = {
        "Toàn bộ mã": (0, 0.0),
        "Thanh khoản ≥ 1 tỷ/phiên": (0, 1.0),
        "Top 100 thanh khoản": (100, 1.0),
    }
    uni_choice = st.selectbox("Phạm vi quét", list(UNI_OPTS), key="uni_choice")
    uni_size, uni_min_val = UNI_OPTS[uni_choice]
    if uni_min_val == 0.0:
        st.caption("⚠️ Model được train trên mã thanh khoản ≥ 1 tỷ/phiên; mã thanh khoản thấp có thể cho xác suất kém tin cậy.")

    n_sym, n_rows, db_last = db_stats()
    db_sig = (n_sym, n_rows, db_last)
    universe, uni_df, uni_failed = [], pd.DataFrame(), []
    top_n = st.slider("Số mã hiển thị", 5, 50, TOP_SHOW, key="top_n")

    if n_sym == 0:
        st.warning("DB chưa có dữ liệu. Chạy `python DB.py import` rồi `python DB.py update`, sau đó tải lại trang.")
    else:
        try:
            universe, _hints = cached_universe(uni_size, uni_min_val, db_sig)
            with st.spinner("Vui lòng chờ trong phút lát..."):
                uni_df, uni_failed = cached_rank(tuple(universe), db_sig)
        except Exception as e:
            st.error(f"Không tính được: {e}")

    if uni_df.empty:
        st.warning("Chưa có kết quả. Kiểm tra DB và model.")
    else:
        top_df = uni_df.head(top_n).reset_index(drop=True)

        def _pred_cls(v):
            return {"Tăng": "tag-up", "Giảm": "tag-down"}.get(v, "tag-flat")

        body = []
        for i, row in top_df.iterrows():
            pu = float(row["P(tăng)"])
            body.append(
                f"<tr><td>{i + 1}</td>"
                f"<td class='sym'>{row['Mã']}</td>"
                f"<td>{row['Sàn']}</td>"
                f"<td>{row['Giá']:.2f}</td>"
                f"<td>{row['Ngày']}</td>"
                f"<td>{row['Trạng thái']}</td>"
                f"<td class='{_pred_cls(row['Dự báo'])}'>{row['Dự báo']}</td>"
                f"<td class='pup'>{pu:.1%}<span class='rank-bar'><i style='width:{pu * 100:.1f}%'></i></span></td></tr>"
            )
        html = (
            TOP_TABLE_CSS
            + "<div class='rank-wrap'><table class='rank-tbl'><thead><tr>"
            + "<th>#</th><th>Mã</th><th>Sàn</th><th>Giá</th><th>Ngày</th><th>Trạng thái</th><th>Dự báo</th><th>Xác suất tăng</th>"
            + "</tr></thead><tbody>" + "".join(body) + "</tbody></table></div>"
        )
        st.markdown(html, unsafe_allow_html=True)
        _latest = uni_df["Ngày"].max()
        _stale = int((uni_df["Ngày"] < _latest).sum())
        st.caption(f"Giá mới nhất: {_latest}"
                   + (f" · {_stale} mã chưa cập nhật được (đang dùng giá cũ trong DB)" if _stale else "")
                   + f" · Quét được {len(uni_df)}/{len(universe)} mã"
                   + (f" · bỏ qua: {', '.join(uni_failed)}" if uni_failed else ""))
        st.download_button("⬇️ Tải CSV top xếp hạng",
                           top_df.to_csv(index=False).encode("utf-8-sig"),
                           "toprank_top_prob_up.csv", "text/csv")
