"""SEPA 1 — Giá > MA(50) > MA(150) > MA(200)."""
from ...indicators import sma
from .config import MA_SHORT, MA_MID, MA_LONG


def check(df):
    c = df["close"]
    p, a, b, d = (float(c.iloc[-1]), float(sma(c, MA_SHORT).iloc[-1]),
                  float(sma(c, MA_MID).iloc[-1]), float(sma(c, MA_LONG).iloc[-1]))
    return {"ok": bool(p > a > b > d), "value": f"{p:.2f} | {a:.2f} | {b:.2f} | {d:.2f}"}
