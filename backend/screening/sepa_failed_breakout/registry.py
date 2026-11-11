"""Danh sách tín hiệu cảnh báo (thêm tín hiệu mới: thêm 1 dòng). ok=True nghĩa là tín hiệu XẤU đang xuất hiện."""
from . import below_ma20, lower_lows, volume_divergence

FAILED_BREAKOUT_SIGNALS = [
    ("1. Đóng cửa dưới MA20", below_ma20.check),
    ("2. 3 đáy thấp hơn", lower_lows.check),
    ("3. Tăng KL thấp / giảm KL cao", volume_divergence.check),
]
