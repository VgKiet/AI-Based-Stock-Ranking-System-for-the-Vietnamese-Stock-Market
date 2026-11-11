"""Phiên giao dịch kỳ vọng đã có dữ liệu."""
import pandas as pd


def expected_last_session():
    """Phiên gần nhất được kỳ vọng đã có dữ liệu đầy đủ (bỏ qua ngày lễ)."""
    now = pd.Timestamp.now()
    today = now.normalize()
    if today.weekday() >= 5 or now.hour < 15:
        return (today - pd.offsets.BDay(1)).normalize()
    return today
