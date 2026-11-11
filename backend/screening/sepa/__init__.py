"""
Bộ lọc kỹ thuật SEPA — mỗi điều kiện 1 file, ngưỡng nằm ở config.py.

    ma_alignment.py        1. Giá > MA50 > MA150 > MA200
    ma200_rising.py        2. MA200 hướng lên ít nhất 1 tháng
    higher_highs_lows.py   3. Chuỗi đỉnh cao hơn, đáy cao hơn
    volume_weeks.py        4. Tuần tăng KL lớn, tuần giảm KL nhỏ
    volume_days.py         5. Số ngày KL tăng > số ngày KL giảm
    off_low.py             6. Giá cao hơn đáy 52W ≥ 30%
    near_high.py           7. Giá thấp hơn đỉnh 52W ≤ 25%
    registry.py            danh sách điều kiện (thêm điều kiện mới ở đây)
    scanner.py             quét toàn thị trường
"""
from .registry import SEPA_CRITERIA
from .scanner import scan_sepa, evaluate_sepa
