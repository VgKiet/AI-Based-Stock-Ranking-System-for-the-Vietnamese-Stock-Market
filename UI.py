"""
UI.py — Điểm vào giao diện Streamlit. Chạy: streamlit run UI.py

  database/  : kho giá SQLite + cập nhật giá mới từ TradingView (chạy riêng: python DB.py update)
  backend/   : chỉ báo + feature + model xu hướng + xếp hạng thị trường (đọc giá từ database)
  frontend/  : styles, components, sections (từng khối hiển thị) và tabs
"""
import streamlit as st

# set_page_config phải là lệnh Streamlit đầu tiên
st.set_page_config(
    page_title="TopRank CK — Nhận diện xu hướng",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from frontend.components import render_hero
from frontend.styles import inject_global_styles
from frontend.tabs import top_rank, stock_detail, sepa, sepa_exit

inject_global_styles()
render_hero()

tab_top, tab_detail, tab_sepa, tab_exit = st.tabs(
    ["🏆  1. Top xác suất tăng", "📈  2. Phân tích 1 mã", "🔎  3. Lọc SEPA", "⚠️  4. Cảnh báo thất bại"]
)

with tab_top:
    top_rank.render()

with tab_detail:
    stock_detail.render()

with tab_sepa:
    sepa.render()

with tab_exit:
    sepa_exit.render()
