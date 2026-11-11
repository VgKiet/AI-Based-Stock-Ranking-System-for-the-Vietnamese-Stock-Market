"""
backend/config.py — Các tham số chỉnh được của phần backend (hằng số model, lọc thanh khoản, mã loại trừ).
Tham số riêng của từng chỉ báo nằm ngay trong file chỉ báo đó (vd indicators/euphoria.py).
"""
from paths import TREND_MODEL_PATH

MODEL_PATH = str(TREND_MODEL_PATH)

CHAN_N = {'D': 120, 'W': 52, 'M': 60}
CHAN_K = 2.0
MIN_BARS_PREDICT = 120      # ít hơn ngần này phiên -> bỏ qua mã

# ============================================================
# LIQUIDITY FILTER
# ============================================================
MIN_PRICE = 2.0             # Giá dưới 2.000 đồng (đơn vị nghìn đồng)
MIN_VOLUME = 50_000
LOOKBACK_SESSIONS = 20
MAX_ZERO_VOLUME_SESSIONS = 2
LOW_VOLUME_SESSIONS = 2
# Mã cổ phiếu loại bỏ cố định
EXCLUDED_SYMBOLS = {"ACM"}
