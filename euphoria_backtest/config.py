"""euphoria_backtest/config.py — Tham số backtest tín hiệu Euphoria cắt lên ngưỡng."""
from pathlib import Path

from paths import DB_PATH as _DB_PATH, BACKTEST_RESULTS_DIR

DB_PATH = Path(_DB_PATH)

MIN_TURNOVER_VND = 1_000_000_000
EUPHORIA_THRESHOLD = 0.8
HORIZONS = (5, 10, 20)

OUTPUT_DIR = BACKTEST_RESULTS_DIR
