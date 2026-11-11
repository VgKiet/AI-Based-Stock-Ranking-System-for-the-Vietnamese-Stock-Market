"""Tín hiệu 3 — Tăng giá khối lượng thấp, giảm giá khối lượng cao (dòng tiền yếu).

Diễn giải: trong 20 phiên gần nhất, KL trung bình của các ngày giá tăng < KL trung bình của các ngày giá giảm.
"""
from .config import VOLUME_LOOKBACK, VOLUME_MAX_RATIO


def check(df):
    d = df.tail(VOLUME_LOOKBACK + 1).copy()
    d["chg"] = d["close"].diff()
    d = d.iloc[1:]
    up, down = d[d["chg"] > 0]["volume"], d[d["chg"] < 0]["volume"]
    if len(up) == 0 or len(down) == 0:
        return {"ok": False, "value": "thiếu ngày tăng/giảm"}
    ratio = float(up.mean() / down.mean())
    return {"ok": bool(ratio < VOLUME_MAX_RATIO), "value": f"KL tăng/giảm x{ratio:.2f}"}
