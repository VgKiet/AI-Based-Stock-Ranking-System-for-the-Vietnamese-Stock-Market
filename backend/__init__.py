"""
backend — Pipeline feature + model xu hướng + xếp hạng thị trường (đọc giá từ package `database`).

Không phụ thuộc Streamlit. Frontend chỉ import package này để lấy kết quả.
Model: model/trend_model_v3.joblib (HistGradientBoosting 3 lớp: Giảm / Đi ngang / Tăng sau H phiên)

Cấu trúc:
    config.py            tham số chỉnh được (kênh hồi quy, lọc thanh khoản, mã loại trừ)
    preprocess.py        chuẩn hoá giá thô về dạng train
    indicators/          mỗi chỉ báo 1 file (MA, MACD, RSI, ADX, kênh hồi quy, hưng phấn)
    features/            ghép chỉ báo thành feature cho model (regime, đa khung, builder)
    prediction/          nạp model + dự đoán xu hướng
    ranking/             lọc thanh khoản + quét/xếp hạng thị trường
"""
from .config import *
from .preprocess import to_daily_indexed
from .indicators import *
from .features import *
from .prediction import load_trend_model, predict_trend
from .ranking import is_low_liquidity, load_universe, scan_universe
from .screening.sepa import SEPA_CRITERIA, scan_sepa, evaluate_sepa
from .screening.sepa_failed_breakout import FAILED_BREAKOUT_SIGNALS, scan_failed_breakout, evaluate_failed_breakout
