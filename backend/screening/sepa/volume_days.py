"""SEPA 5 — Số ngày khối lượng tăng nhiều hơn số ngày khối lượng giảm.

Diễn giải: "ngày khối lượng tăng" = ngày giá tăng với KL > trung bình 20 phiên (gom hàng),
           "ngày khối lượng giảm" = ngày giá giảm với KL > trung bình 20 phiên (xả hàng).
"""
from .config import VOLUME_DAYS_LOOKBACK, VOLUME_AVG_WINDOW


def check(df):
    avg = df["volume"].rolling(VOLUME_AVG_WINDOW).mean().shift(1)
    heavy = df["volume"] > avg
    chg = df["close"].diff()
    up = int(((chg > 0) & heavy).tail(VOLUME_DAYS_LOOKBACK).sum())
    down = int(((chg < 0) & heavy).tail(VOLUME_DAYS_LOOKBACK).sum())
    return {"ok": bool(up > down), "value": f"{up} tăng / {down} giảm"}
