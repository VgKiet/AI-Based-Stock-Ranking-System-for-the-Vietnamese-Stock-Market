"""frontend/styles.py — Toàn bộ CSS của giao diện. Muốn đổi màu/kiểu chữ thì sửa ở đây."""
import streamlit as st

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Be Vietnam Pro','Inter','Segoe UI',sans-serif; }
.main { background: #f4f6fb; }
#MainMenu {visibility:hidden;} footer {visibility:hidden;}
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1350px; }
.hero {
  background: radial-gradient(1200px 400px at 10% 0%, #2b6cb0 0%, transparent 60%),
              linear-gradient(135deg, #0b1e3a 0%, #143a6b 55%, #1c4a8a 100%);
  border-radius: 18px; padding: 26px 30px; color: #fff;
  box-shadow: 0 12px 32px rgba(11,30,58,.25); margin-bottom: 18px;
  border: 1px solid rgba(255,255,255,.12); position: relative; overflow: hidden;
}
.hero h1 { margin:0; font-size:28px; font-weight:800; }
.hero h1 .brand { background:#ffd34d; color:#0b1e3a; padding:2px 10px; border-radius:9px; margin-right:8px;}
.hero p { margin:8px 0 0 0; color:#cfe0f5; font-size:13.5px; }
.hero-meta { display:flex; gap:10px; margin-top:14px; flex-wrap:wrap; }
.hero-chip { background: rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.18);
  padding:6px 12px; border-radius:999px; font-size:12.5px; font-weight:600; color:#fff; }
.hero-chip b { color:#ffd34d; }
.card { background:#fff; border:1px solid #e6ebf3; border-radius:16px; padding:18px;
  box-shadow: 0 4px 16px rgba(15,39,72,.06); }
.section-title { font-size:16px; font-weight:800; color:#0f2748; margin:4px 0 12px 0;
  border-left:5px solid #1c4a8a; padding-left:10px; }
.section-sub { font-size:12.5px; color:#6b7280; margin:-6px 0 12px 0; }
div[data-testid="stMetric"] { background:#fff; border:1px solid #e6ebf3; border-radius:14px;
  padding:14px 16px; box-shadow: 0 2px 10px rgba(15,39,72,.05); }
.badge { display:inline-block; padding:5px 13px; border-radius:999px; font-weight:700; font-size:12.5px; white-space:nowrap;}
.badge-up { background:#e6f7ee; color:#0f9d58; border:1px solid #b9e8cd;}
.badge-down { background:#fdecec; color:#d93025; border:1px solid #f5c6c2;}
.badge-flat { background:#eef2f7; color:#5f6b7a; border:1px solid #d7dfea;}
.badge-info { background:#e8f0fe; color:#1a56db; border:1px solid #c2d6fd;}
.badge-san { background:#0f2748; color:#ffd34d; border:1px solid #0f2748; font-size:11.5px;}
section[data-testid="stSidebar"] { background: linear-gradient(180deg,#0b1e3a 0%, #10294f 100%); }
section[data-testid="stSidebar"] * { color:#eaf1fb !important; }
section[data-testid="stSidebar"] input, section[data-testid="stSidebar"] textarea {
  color:#0f2748 !important; background:#fff !important; border-radius:10px !important; }
section[data-testid="stSidebar"] div[data-baseweb="select"] span { color:#0f2748 !important; }
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
  background:#fff !important; border-radius:10px !important; }
section[data-testid="stSidebar"] button p, section[data-testid="stSidebar"] button span { color:#0f2748 !important; }
.sidebar-brand { background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.14);
  border-radius:14px; padding:14px; margin-bottom:14px; }
.sidebar-brand h3 { margin:0; font-size:17px; font-weight:800; color:#fff !important;}
.sidebar-brand small { color:#9fb6d8 !important; font-size:12px;}
button[data-baseweb="tab"] { font-weight:700 !important; font-size:14px !important; }
div[data-testid="stButton"] > button { border-radius:11px !important; font-weight:700 !important; }
div[data-testid="stDataFrame"] { border-radius:14px; overflow:hidden; border:1px solid #e6ebf3; }
.disclaimer { background:#fff8e6; border:1px solid #ffe3a3; border-radius:12px;
  padding:12px 16px; font-size:12.5px; color:#6b5300; margin-top:16px; }
.prob-bar { height:10px; border-radius:99px; background:#eef2f7; overflow:hidden; }
</style>
"""

HIDE_SIDEBAR_CSS = (
    "<style>[data-testid='stSidebar'],[data-testid='stSidebarCollapsedControl'],"
    "[data-testid='collapsedControl']{display:none !important;}</style>"
)

TOP_TABLE_CSS = """
<style>
.rank-wrap { background:#0e1117; border-radius:14px; padding:6px 4px; overflow-x:auto;
  border:1px solid #1f2430; box-shadow:0 4px 16px rgba(15,39,72,.15); }
table.rank-tbl { width:100%; border-collapse:collapse; font-size:14px; color:#e6e9ef; }
table.rank-tbl th { text-align:left; color:#9aa3b2; font-weight:700; font-size:12.5px;
  text-transform:uppercase; padding:12px 14px; border-bottom:1px solid #1f2430; white-space:nowrap; }
table.rank-tbl td { padding:10px 14px; white-space:nowrap; }
table.rank-tbl tr:nth-child(odd) td { background:#12161f; }
table.rank-tbl tr:nth-child(even) td { background:#0e1117; }
table.rank-tbl tr:hover td { background:#1a2030; }
table.rank-tbl td.sym { font-weight:800; color:#fff; }
table.rank-tbl td.pup { font-weight:800; color:#b66dff; }
.rank-bar { display:inline-block; vertical-align:middle; width:110px; height:8px; margin-left:10px;
  background:#262c3a; border-radius:99px; overflow:hidden; }
.rank-bar > i { display:block; height:100%; background:#0f9d58; }
.tag-up { color:#2ecc71; font-weight:700; } .tag-down { color:#ff5c5c; font-weight:700; }
.tag-flat { color:#9aa3b2; font-weight:700; }
</style>
"""


def inject_global_styles():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(HIDE_SIDEBAR_CSS, unsafe_allow_html=True)
