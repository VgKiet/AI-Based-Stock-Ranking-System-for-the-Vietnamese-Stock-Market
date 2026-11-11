"""Bảng feature đầu vào model (dòng cuối)."""
import streamlit as st

from backend import load_trend_model


def render(r):
    st.markdown('<div class="section-title">🧬 Feature model (dòng cuối)</div>', unsafe_allow_html=True)
    feats = r["features"]
    _, feat_names, _, _ = load_trend_model()
    last_feat = feats[feat_names].iloc[-1].round(4).rename("giá trị").to_frame()
    st.dataframe(last_feat, width="stretch", height=380)
