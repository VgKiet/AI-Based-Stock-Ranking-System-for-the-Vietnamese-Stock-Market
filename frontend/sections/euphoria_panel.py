"""Chỉ báo hưng phấn thị trường [-1, 1]: thẻ điểm + bảng thành phần + biểu đồ."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from backend import (
    euphoria_index, euphoria_zone,
    EUPHORIA_HI, EUPHORIA_LO, EUPHORIA_LABELS,
)


def render(code, df_daily):
    # Hưng phấn thị trường [-1, 1]
    st.markdown('<div class="section-title">🔥 Chỉ báo hưng phấn thị trường [-1, 1]</div>', unsafe_allow_html=True)
    if len(df_daily) < 130:
        st.info(f"Cần tối thiểu ~130 phiên để tính chỉ báo hưng phấn, {code} mới có {len(df_daily)} phiên.")
    else:
        eu = euphoria_index(df_daily)
        eu_last = float(eu["euphoria"].iloc[-1])
        eu_prev = float(eu["euphoria"].iloc[-2]) if len(eu) > 1 else eu_last
        eu_label, eu_color = euphoria_zone(eu_last)

        e1, e2 = st.columns([1, 2.2])
        with e1:
            st.markdown(
                f"""<div class="card" style="text-align:center;">
                <div style="font-size:13px;color:#6b7280;">Mức hưng phấn {code}</div>
                <div style="font-size:44px;font-weight:800;color:{eu_color};line-height:1.15;">{eu_last:+.2f}</div>
                <div style="font-weight:700;color:{eu_color};">{eu_label}</div>
                <div style="font-size:12.5px;color:#6b7280;margin-top:6px;">Hôm qua {eu_prev:+.2f} · thay đổi {eu_last - eu_prev:+.2f}</div>
                </div>""",
                unsafe_allow_html=True,
            )
            comp_last = eu[list(EUPHORIA_LABELS)].iloc[-1]
            st.dataframe(
                pd.DataFrame({"Thành phần": [EUPHORIA_LABELS[k] for k in comp_last.index],
                              "Giá trị": comp_last.round(2).values}),
                hide_index=True, width="stretch")
        with e2:
            eplot = eu.tail(150)
            efig = go.Figure()
            efig.add_hrect(y0=EUPHORIA_HI, y1=1, fillcolor="rgba(38,166,154,0.10)", line_width=0)
            efig.add_hrect(y0=-1, y1=EUPHORIA_LO, fillcolor="rgba(239,83,80,0.10)", line_width=0)
            efig.add_trace(go.Scatter(x=eplot.index, y=eplot["euphoria"].clip(lower=0), mode="none", showlegend=False,
                                      fill="tozeroy", fillcolor="rgba(38,166,154,0.25)", hoverinfo="skip"))
            efig.add_trace(go.Scatter(x=eplot.index, y=eplot["euphoria"].clip(upper=0), mode="none", showlegend=False,
                                      fill="tozeroy", fillcolor="rgba(239,83,80,0.25)", hoverinfo="skip"))
            efig.add_trace(go.Scatter(x=eplot.index, y=eplot["euphoria"], mode="lines", name="Hưng phấn",
                                      line=dict(color="#7e57c2", width=2), hovertemplate="%{x|%d/%m/%Y}: %{y:+.2f}<extra></extra>"))
            efig.add_hline(y=1, line=dict(color="#26a69a", dash="dash", width=1))
            efig.add_hline(y=0, line=dict(color="#9aa3b2", dash="dot", width=1))
            efig.add_hline(y=-1, line=dict(color="#ef5350", dash="dash", width=1))
            efig.add_hline(y=EUPHORIA_HI, line=dict(color="#26a69a", dash="dot", width=1))
            efig.add_hline(y=EUPHORIA_LO, line=dict(color="#ef5350", dash="dot", width=1))
            efig.update_yaxes(range=[-1.05, 1.05], tickvals=[-1, EUPHORIA_LO, 0, EUPHORIA_HI, 1])
            efig.update_layout(template="plotly_white", height=330, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
            st.plotly_chart(efig, width="stretch")
        st.caption("Gộp 5 thành phần (độ giãn giá, RSI, vị trí trong vùng giá, áp lực khối lượng, động lượng ROC). "
                   "≥ +0.8: hưng phấn quá mức (dễ nóng) · ≤ −0.8: bi quan cực độ (dễ hồi). Chỉ mang tính tham khảo.")
    st.write("")
