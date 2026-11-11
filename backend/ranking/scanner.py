"""Quét toàn thị trường: chạy model cho từng mã và xếp hạng theo P(tăng)."""
import pandas as pd

import database

from ..config import EXCLUDED_SYMBOLS, MIN_BARS_PREDICT
from ..preprocess import to_daily_indexed
from ..prediction import predict_trend
from .liquidity import is_low_liquidity


def load_universe(size: int = 0, min_value_bn: float = 0.0):
    """Danh sách mã lấy từ database. size=0 -> tất cả. min_value_bn = lọc thanh khoản (tỷ đồng/phiên).
    Trả (symbols, {mã: sàn})."""
    return database.db_universe(size, min_value_bn)


def scan_universe(symbols, n_bars: int = 1500, progress=None):
    """Chạy model cho từng mã từ giá trong DB (KHÔNG gọi mạng). Trả (DataFrame xếp hạng theo P(tăng), [mã lỗi])."""
    symbols = [
    code for code in symbols
    if code.upper() not in EXCLUDED_SYMBOLS
    ]
    meta = database.db_meta_all()
    rows, failed = [], []
    for i, code in enumerate(symbols):
        try:
            df_raw = database.db_read(code, n_bars)
            if df_raw is None or df_raw.empty:
                failed.append(f"{code} (không có dữ liệu)")
                continue
            df_daily = to_daily_indexed(df_raw)

            if len(df_daily) < MIN_BARS_PREDICT:
                failed.append(f"{code} (ít nến)")
                continue

            # Liquidity Filter
            if is_low_liquidity(df_daily):
                failed.append(f"{code} (thanh khoản thấp)")
                continue

            r = predict_trend(df_daily)
            rows.append({
                "Mã": code, "Sàn": meta.get(code, (None, 0, None))[2],
                "Giá": round(float(df_daily["close"].iloc[-1]), 2),
                "Ngày": df_daily.index[-1].strftime("%Y-%m-%d"),
                "Trạng thái": r["regime"], "Dự báo": r["pred_name"],
                "P(tăng)": round(r["p_up"], 4), "P(ngang)": round(r["p_flat"], 4), "P(giảm)": round(r["p_down"], 4),
            })
        except Exception as e:
            failed.append(f"{code} (lỗi tính: {type(e).__name__})")
        if progress is not None and (i + 1) % 25 == 0:
            progress(i + 1, len(symbols))
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("P(tăng)", ascending=False).reset_index(drop=True)
    return df, failed
