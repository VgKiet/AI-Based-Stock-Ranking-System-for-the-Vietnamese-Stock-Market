"""Tín hiệu 1 — Giá đóng cửa dưới MA(20)."""
from ...indicators import sma
from .config import MA_PERIOD


def check(df):
    c = float(df["close"].iloc[-1])
    ma = float(sma(df["close"], MA_PERIOD).iloc[-1])
    return {"ok": bool(c < ma), "value": f"{c:.2f} vs MA20 {ma:.2f} ({(c / ma - 1) * 100:+.1f}%)"}
