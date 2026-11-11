"""Thẻ tổng quan mã: sàn, H phiên, giá, thay đổi, trạng thái."""
import pandas as pd
import streamlit as st

from ..components import regime_badge


def render(code, selected_exchange, price, chg, r, df_daily):
    st.markdown(
        f"""<div class="card" style="margin-bottom:14px;">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
          <div>
            <span class="badge badge-san">{selected_exchange}</span>
            <span class="badge badge-info" style="margin-left:6px;">H={r['H']} phiên · ±{r['UP_T']*100:.0f}%</span>
            <h2 style="margin:8px 0 2px 0;color:#0f2748;">{code}
              <small style="color:#6b7280;">· {price:.2f} ({chg:+.2f}%)</small></h2>
            <div style="font-size:12.5px;color:#6b7280;">Dữ liệu tới <b>{pd.to_datetime(r['last_time']).strftime('%d/%m/%Y')}</b> · {len(df_daily)} nến ngày</div>
          </div>
          <div>{regime_badge(r['regime'])}</div>
        </div></div>""",
        unsafe_allow_html=True,
    )
