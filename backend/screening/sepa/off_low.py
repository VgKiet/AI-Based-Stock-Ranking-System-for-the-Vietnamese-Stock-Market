"""SEPA 6 — Giá hiện tại cao hơn đáy 52 tuần ít nhất 30%."""
from .config import MIN_ABOVE_LOW_PCT, WEEKS_52


def check(df):
    low = float((df["low"] if "low" in df else df["close"]).tail(WEEKS_52).min())
    pct = (float(df["close"].iloc[-1]) / low - 1) * 100
    return {"ok": bool(pct >= MIN_ABOVE_LOW_PCT), "value": f"+{pct:.1f}% so với đáy"}
