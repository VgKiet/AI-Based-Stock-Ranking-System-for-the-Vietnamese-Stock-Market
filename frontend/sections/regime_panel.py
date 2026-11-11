"""Trạng thái đa khung D/W/M + kênh hồi quy + RSI/ADX/gãy MA50 (đúng logic train)."""
import pandas as pd
import streamlit as st


def render(r):
    st.markdown('<div class="section-title">📌 Trạng thái đa khung (đúng logic train)</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        - Trạng thái: **{r['regime']}**
        - Hướng D/W/M: **D={int(r['D']) if pd.notna(r['D']) else '—'} · W={int(r['W']) if pd.notna(r['W']) else '—'} · M={int(r['M']) if pd.notna(r['M']) else '—'}** (1=tăng, 0=giảm)
        - Kênh hồi quy (0=hỗ trợ, 1=kháng cự): D={r['chan_d']:.2f} · W={r['chan_w']:.2f} · M={r['chan_m']:.2f}
        - RSI D (Wilder): **{float(r['rsi_d']):.1f}** · ADX: **{float(r['adx_d']):.1f}** {'(sideway, dễ nhiễu)' if pd.notna(r['sideways']) and r['sideways'] == 1 else ''}
        - RSI 2 đáy: **{'Có' if r['rsi_hl'] == 1 else 'Không'}** · Phân kỳ dương: **{'Có' if r['rsi_div'] == 1 else 'Không'}**
        - Gãy MA50: **{'Có' if r['break50'] == 1 else 'Không'}** · Gãy mạnh: **{'Có' if r['break50_strong'] == 1 else 'Không'}**
        """
    )
    st.caption("Cách đọc như notebook: D/W/M=1 là tăng; kênh ~0 là sát hỗ trợ, ~1 sát kháng cự, âm là lủng. "
               "VD tháng giảm (M=0) nhưng kênh M thấp = giảm nhưng tại hỗ trợ, có thể hồi.")
