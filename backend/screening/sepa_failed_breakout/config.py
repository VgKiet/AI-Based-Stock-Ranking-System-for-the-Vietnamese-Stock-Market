"""Tham số cảnh báo "break out thất bại" (SEPA) — sửa ngưỡng ở đây."""
MIN_BARS = 60

# 1. Giá đóng cửa dưới MA(20)
MA_PERIOD = 20

# 2. 3 đáy thấp hơn
PIVOT_ORDER = 3          # nhạy hơn bộ lọc SEPA chính (±3 phiên) để cảnh báo sớm
PIVOT_LOOKBACK = 60
PIVOT_COUNT = 3

# 3. Tăng giá khối lượng thấp, giảm giá khối lượng cao
VOLUME_LOOKBACK = 20     # xét 20 phiên gần nhất
VOLUME_MAX_RATIO = 1.0   # KL TB ngày tăng / KL TB ngày giảm phải < ngưỡng này

# Mức cảnh báo theo số tín hiệu xuất hiện cùng lúc
ALERT_LEVELS = {0: "Bình thường", 1: "Theo dõi", 2: "Cân nhắc cắt lỗ", 3: "Cắt lỗ sớm"}
