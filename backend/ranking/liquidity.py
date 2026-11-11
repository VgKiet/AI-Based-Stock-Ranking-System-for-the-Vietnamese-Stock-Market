"""Bộ lọc thanh khoản (Penny Filter)."""
from ..config import (
    MIN_PRICE, MIN_VOLUME, LOOKBACK_SESSIONS,
    MAX_ZERO_VOLUME_SESSIONS, LOW_VOLUME_SESSIONS,
)


def is_low_liquidity(df):
    """
    Penny Filter:

    1. Giá dưới 2.000 đồng.
    2. Có >= 2 phiên Volume = 0 trong 20 phiên gần nhất.
    3. Có 2 phiên liên tiếp Volume < 50.000 CP.
    """

    if df is None or df.empty:
        return True

    # Điều kiện 1: Giá dưới 2.000 đồng
    latest_price = float(df["close"].iloc[-1])

    if latest_price < MIN_PRICE:
        return True

    # Cần đủ 20 phiên để đánh giá thanh khoản
    if len(df) < LOOKBACK_SESSIONS:
        return True

    recent = df.tail(LOOKBACK_SESSIONS)
    volume = recent["volume"]

    if volume.isna().any():
        return True

    # Điều kiện 2: Có ít nhất 2 phiên không giao dịch
    zero_sessions = (volume == 0).sum()

    if zero_sessions >= MAX_ZERO_VOLUME_SESSIONS:
        return True

    # Điều kiện 3: 2 phiên liên tiếp dưới 50.000 CP
    if (volume.tail(LOW_VOLUME_SESSIONS) < MIN_VOLUME).all():
        return True

    return False
