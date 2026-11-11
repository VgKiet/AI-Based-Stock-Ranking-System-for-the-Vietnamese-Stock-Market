"""SEPA 4 — Tuần tăng giá có khối lượng lớn, tuần giảm giá có khối lượng nhỏ."""
from .config import VOLUME_WEEKS_LOOKBACK, VOLUME_WEEKS_MIN_RATIO


def check(df):
    w = df.resample("W-FRI").agg({"close": "last", "volume": "sum"}).dropna()
    w["ret"] = w["close"].pct_change()
    w = w.tail(VOLUME_WEEKS_LOOKBACK)
    up, down = w[w["ret"] > 0]["volume"], w[w["ret"] < 0]["volume"]
    if len(up) == 0 or len(down) == 0:
        return {"ok": False, "value": "thiếu tuần tăng/giảm"}
    ratio = float(up.mean() / down.mean())
    return {"ok": bool(ratio > VOLUME_WEEKS_MIN_RATIO), "value": f"x{ratio:.2f}"}
