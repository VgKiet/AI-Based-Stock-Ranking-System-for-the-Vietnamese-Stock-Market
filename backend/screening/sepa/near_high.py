"""SEPA 7 — Giá hiện tại thấp hơn đỉnh 52 tuần không quá 25%."""
from .config import MAX_BELOW_HIGH_PCT, WEEKS_52


def check(df):
    high = float((df["high"] if "high" in df else df["close"]).tail(WEEKS_52).max())
    pct = (float(df["close"].iloc[-1]) / high - 1) * 100
    return {"ok": bool(pct >= -MAX_BELOW_HIGH_PCT), "value": f"{pct:.1f}% so với đỉnh"}
