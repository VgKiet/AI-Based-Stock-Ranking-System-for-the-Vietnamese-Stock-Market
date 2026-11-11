"""
SEPA — Cảnh báo break out thất bại (xem xét cụm tín hiệu, có thể cắt lỗ sớm). Mỗi tín hiệu 1 file.

    below_ma20.py          1. Giá đóng cửa dưới MA(20)
    lower_lows.py          2. 3 đáy thấp hơn
    volume_divergence.py   3. Tăng giá KL thấp, giảm giá KL cao
    registry.py            danh sách tín hiệu | scanner.py quét thị trường | config.py ngưỡng
"""
from .registry import FAILED_BREAKOUT_SIGNALS
from .scanner import scan_failed_breakout, evaluate_failed_breakout
