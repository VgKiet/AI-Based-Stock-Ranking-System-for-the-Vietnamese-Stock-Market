"""
paths.py — Đường dẫn dùng chung cho cả dự án. Muốn đổi vị trí file/thư mục thì sửa ở đây.
"""
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

DATA_DIR = ROOT_DIR / "data"
MODEL_DIR = ROOT_DIR / "model"
BACKTEST_RESULTS_DIR = ROOT_DIR / "backtest_results"

DB_PATH = DATA_DIR / "prices.db"
UNIVERSE_CSV = DATA_DIR / "data_full_market.csv"
TREND_MODEL_PATH = MODEL_DIR / "trend_model_v3.joblib"
ENV_PATH = ROOT_DIR / ".env"
