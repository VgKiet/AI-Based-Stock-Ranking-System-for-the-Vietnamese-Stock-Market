"""Danh sách điều kiện SEPA (thứ tự = thứ tự cột hiển thị). Thêm điều kiện mới: thêm 1 dòng ở đây."""
from . import (ma_alignment, ma200_rising, higher_highs_lows,
               volume_weeks, volume_days, off_low, near_high)
from .config import MIN_ABOVE_LOW_PCT, MAX_BELOW_HIGH_PCT

# (tên cột hiển thị, hàm check(df) -> {"ok": bool, "value": str})
SEPA_CRITERIA = [
    ("1. Giá>MA50>MA150>MA200", ma_alignment.check),
    ("2. MA200 hướng lên 1 tháng", ma200_rising.check),
    ("3. Đỉnh & đáy cao dần", higher_highs_lows.check),
    ("4. Tuần tăng KL lớn", volume_weeks.check),
    ("5. Ngày KL tăng > giảm", volume_days.check),
    (f"6. Cách đáy 52W ≥ {MIN_ABOVE_LOW_PCT:g}%", off_low.check),
    (f"7. Cách đỉnh 52W ≤ {MAX_BELOW_HIGH_PCT:g}%", near_high.check),
]
