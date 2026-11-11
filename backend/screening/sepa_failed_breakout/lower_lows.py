"""Tín hiệu 2 — 3 đáy thấp hơn (3 đáy liên tiếp, mỗi đáy thấp hơn đáy trước)."""
import numpy as np

from ..sepa.higher_highs_lows import find_pivots
from .config import PIVOT_ORDER, PIVOT_LOOKBACK, PIVOT_COUNT


def check(df):
    d = df.tail(PIVOT_LOOKBACK + PIVOT_ORDER)
    lows = find_pivots(d["low"] if "low" in d else d["close"], PIVOT_ORDER, "low").tail(PIVOT_COUNT)
    if len(lows) < PIVOT_COUNT:
        return {"ok": False, "value": f"chưa đủ {PIVOT_COUNT} đáy"}
    ok = bool(np.all(np.diff(lows.values) < 0))
    return {"ok": ok, "value": " → ".join(f"{v:.2f}" for v in lows.values)}
