"""database/config.py — Đường dẫn DB/CSV và các hằng số cập nhật giá."""
from paths import DB_PATH as _DB_PATH, UNIVERSE_CSV as _UNIVERSE_CSV

EXCHANGES = ["HOSE", "HNX", "UPCOM"]

UNIVERSE_CSV = str(_UNIVERSE_CSV)
DB_PATH = str(_DB_PATH)
DB_MIN_BARS = 1000      # DB có >= ngần này phiên của 1 mã thì chỉ cần cập nhật phần mới
