"""
Tham số bộ lọc SEPA — sửa ngưỡng ở đây (1 tuần = 5 phiên).
"""
MIN_BARS = 252                 # cần ít nhất ~1 năm dữ liệu (để tính MA200 và đỉnh/đáy 52 tuần)

# 1. Giá > MA50 > MA150 > MA200
MA_SHORT, MA_MID, MA_LONG = 50, 150, 200

# 2. MA200 hướng lên ít nhất 1 tháng
MA200_RISING_SESSIONS = 21     # 1 tháng ≈ 21 phiên

# 3. Chuỗi đỉnh cao hơn, đáy cao hơn
PIVOT_ORDER = 5                # 1 đỉnh/đáy = cao/thấp nhất trong ±5 phiên (≈ 1 tuần mỗi bên)
PIVOT_LOOKBACK = 120           # chỉ xét ~6 tháng gần nhất
PIVOT_COUNT = 3                # cần ít nhất 3 đỉnh và 3 đáy liên tiếp, mỗi cái cao hơn cái trước

# 4. Tuần tăng khối lượng lớn, tuần giảm khối lượng nhỏ
VOLUME_WEEKS_LOOKBACK = 13     # ~1 quý
VOLUME_WEEKS_MIN_RATIO = 1.0   # KL trung bình tuần tăng / KL trung bình tuần giảm phải > ngưỡng này

# 5. Số ngày khối lượng "tăng" nhiều hơn số ngày khối lượng "giảm"
VOLUME_DAYS_LOOKBACK = 50
VOLUME_AVG_WINDOW = 20         # ngày có KL > trung bình 20 phiên mới tính là ngày KL lớn

# 6. Giá hiện tại cao hơn đáy 52 tuần ít nhất ...%
MIN_ABOVE_LOW_PCT = 30.0
# 7. Giá hiện tại thấp hơn đỉnh 52 tuần không quá ...%
MAX_BELOW_HIGH_PCT = 25.0
WEEKS_52 = 252                 # 52 tuần = 252 phiên
