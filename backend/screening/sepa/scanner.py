"""Quét thị trường theo bộ lọc SEPA (chỉ đọc giá từ DB, không gọi mạng)."""
import pandas as pd

import database

from ...config import EXCLUDED_SYMBOLS
from ...preprocess import to_daily_indexed
from ...ranking.liquidity import is_low_liquidity
from .config import MIN_BARS
from .registry import SEPA_CRITERIA


def evaluate_sepa(df_daily):
    """Chạy cả 7 điều kiện cho 1 mã. Trả {tên điều kiện: {"ok", "value"}}."""
    return {name: fn(df_daily) for name, fn in SEPA_CRITERIA}


def scan_sepa(symbols, n_bars: int = 400, progress=None):
    """Trả (DataFrame, [mã lỗi/bị loại]). Mỗi điều kiện 1 cột ✓/✗, sắp xếp theo số điều kiện đạt."""
    symbols = [c for c in symbols if c.upper() not in EXCLUDED_SYMBOLS]
    meta = database.db_meta_all()
    rows, failed = [], []
    for i, code in enumerate(symbols):
        try:
            df_raw = database.db_read(code, n_bars)
            if df_raw is None or df_raw.empty:
                failed.append(f"{code} (không có dữ liệu)")
                continue
            df = to_daily_indexed(df_raw)
            if len(df) < MIN_BARS:
                failed.append(f"{code} (ít nến)")
                continue
            if is_low_liquidity(df):
                failed.append(f"{code} (thanh khoản thấp)")
                continue
            res = evaluate_sepa(df)
            n_ok = sum(r["ok"] for r in res.values())
            row = {
                "Mã": code, "Sàn": meta.get(code, (None, 0, None))[2],
                "Giá": round(float(df["close"].iloc[-1]), 2),
                "Ngày": df.index[-1].strftime("%Y-%m-%d"),
                "Số ĐK đạt": n_ok, "Đạt đủ": n_ok == len(res),
            }
            for name, r in res.items():
                row[name] = r["ok"]
            for name, r in res.items():
                row[name + " | chi tiết"] = r["value"]
            rows.append(row)
        except Exception as e:
            failed.append(f"{code} (lỗi tính: {type(e).__name__})")
        if progress is not None and (i + 1) % 25 == 0:
            progress(i + 1, len(symbols))
    df_out = pd.DataFrame(rows)
    if not df_out.empty:
        df_out = df_out.sort_values(["Số ĐK đạt", "Mã"], ascending=[False, True]).reset_index(drop=True)
    return df_out, failed
