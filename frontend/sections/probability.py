"""4 ô metric xác suất + thanh xác suất Tăng / Đi ngang / Giảm."""
import streamlit as st


def render(r):
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("P(Tăng)", f"{r['p_up']:.3f}", r["pred_name"] if r["pred"] == 2 else None)
    m2.metric("P(Đi ngang)", f"{r['p_flat']:.3f}")
    m3.metric("P(Giảm)", f"{r['p_down']:.3f}")
    m4.metric("Kết luận model", r["pred_name"])

    # Thanh xác suất
    st.markdown(
        f"""<div class="card">
        <b>Xác suất xu hướng sau {r['H']} phiên</b>
        <div style="margin-top:10px;font-size:13px;">📈 Tăng {r['p_up']:.1%}</div>
        <div class="prob-bar"><div style="width:{r['p_up']*100:.1f}%;height:100%;background:#0f9d58;"></div></div>
        <div style="margin-top:8px;font-size:13px;">➖ Đi ngang {r['p_flat']:.1%}</div>
        <div class="prob-bar"><div style="width:{r['p_flat']*100:.1f}%;height:100%;background:#9aa3b2;"></div></div>
        <div style="margin-top:8px;font-size:13px;">📉 Giảm {r['p_down']:.1%}</div>
        <div class="prob-bar"><div style="width:{r['p_down']*100:.1f}%;height:100%;background:#d93025;"></div></div>
        </div>""",
        unsafe_allow_html=True,
    )
    st.write("")
