"""Cảnh báo miễn trừ trách nhiệm."""
import streamlit as st


def render(r):
    st.markdown(
        f"""<div class="disclaimer">⚠️ Model phân loại xu hướng sau {r['H']} phiên (Tăng ≥ +{r['UP_T']*100:.0f}% / Giảm ≤ −{r['UP_T']*100:.0f}% / còn lại Đi ngang).
        Chỉ mang tính tham khảo, không phải khuyến nghị mua/bán. Dùng cùng bảng kiểm tra lợi thế theo regime trong notebook.</div>""",
        unsafe_allow_html=True,
    )
