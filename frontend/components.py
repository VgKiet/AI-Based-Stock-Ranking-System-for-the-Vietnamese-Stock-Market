"""Thành phần giao diện dùng chung: badge trạng thái, hero header."""
from datetime import datetime

import streamlit as st


def regime_badge(regime: str) -> str:
    up_keys = ["Tăng mạnh", "Hồi mạnh"]
    down_keys = ["Giảm mạnh", "Điều chỉnh sâu", "GÃY MA50"]
    if any(k in regime for k in up_keys):
        cls, icon = "badge-up", "📈"
    elif any(k in regime for k in down_keys):
        cls, icon = "badge-down", "📉"
    else:
        cls, icon = "badge-flat", "↔️"
    return f'<span class="badge {cls}">{icon} {regime}</span>'


def render_hero():
    now_str = datetime.now().strftime("%H:%M · %d/%m/%Y")
    st.markdown(
        f"""
        <div class="hero">
          <h1><span class="brand">TopRank</span> Nhận diện xu hướng cổ phiếu VN</h1>
          <p>Model phân loại 3 xu hướng sau H phiên: <b>Tăng / Đi ngang / Giảm</b> — theo đúng pipeline train đa khung D/W/M + kênh hồi quy.</p>
          <div class="hero-meta">
            <span class="hero-chip">🕒 <b>{now_str}</b></span>
            <span class="hero-chip">🗄️ <b>Dữ liệu DB</b> · HOSE/HNX/UPCOM</span>
            <span class="hero-chip">🧠 <b>trend_model_v3</b></span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
