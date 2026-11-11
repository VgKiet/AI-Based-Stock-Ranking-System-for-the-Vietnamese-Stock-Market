"""Biểu đồ nến ngày + MA10/MA50 + Volume."""
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots


def render(df_daily):
    # Nến + MA
    st.markdown('<div class="section-title">🕯️ Nến giá · MA10/MA50 · Volume</div>', unsafe_allow_html=True)
    dplot = df_daily.tail(150)
    ma10 = dplot["close"].rolling(10).mean()
    ma50 = dplot["close"].rolling(50).mean()
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.72, 0.28], vertical_spacing=0.06)
    fig.add_trace(go.Candlestick(x=dplot.index, open=dplot["open"], high=dplot["high"],
                                 low=dplot["low"], close=dplot["close"], name="Nến ngày",
                                 increasing_line_color="#0f9d58", decreasing_line_color="#d93025"), row=1, col=1)
    fig.add_trace(go.Scatter(x=dplot.index, y=ma10, mode="lines", name="MA10"), row=1, col=1)
    fig.add_trace(go.Scatter(x=dplot.index, y=ma50, mode="lines", name="MA50",
                             line=dict(dash="dot")), row=1, col=1)
    if "volume" in dplot.columns:
        colors = ["#0f9d58" if c >= o else "#d93025" for c, o in zip(dplot["close"], dplot["open"])]
        fig.add_trace(go.Bar(x=dplot.index, y=dplot["volume"], name="Volume",
                             marker_color=colors, opacity=0.6), row=2, col=1)
    fig.update_layout(template="plotly_white", height=500, margin=dict(l=10, r=10, t=30, b=10),
                      legend=dict(orientation="h", y=1.02, x=1, xanchor="right"),
                      xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, width="stretch")
