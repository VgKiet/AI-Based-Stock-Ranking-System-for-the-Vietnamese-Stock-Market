"""Quét cảnh báo break out thất bại (chỉ đọc giá từ DB, không gọi mạng)."""
import pandas as pd

import database

from ...config import EXCLUDED_SYMBOLS
from ...preprocess import to_daily_indexed
from ...ranking.liquidity import is_low_liquidity
from .config import MIN_BARS, ALERT_LEVELS
from .registry import FAILED_BREAKOUT_SIGNALS


def evaluate_failed_breakout(df_daily):
    return {name: fn(df_daily) for name, fn in FAILED_BREAKOUT_SIGNALS}


def scan_failed_breakout(symbols, n_bars: int = 200, check_liquidity: bool = True, progress=None):
    """Trả (DataFrame sắp xếp theo số tín hiệu giảm dần, [mã lỗi/bị loại]).
    check_liquidity=False dùng khi quét danh sách mã đang nắm giữ (không loại mã thanh khoản thấp)."""
    if check_liquidity:
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
            if check_liquidity and is_low_liquidity(df):
                failed.append(f"{code} (thanh khoản thấp)")
                continue
            res = evaluate_failed_breakout(df)
            n = sum(r["ok"] for r in res.values())
            row = {
                "Mã": code, "Sàn": meta.get(code, (None, 0, None))[2],
                "Giá": round(float(df["close"].iloc[-1]), 2),
                "Ngày": df.index[-1].strftime("%Y-%m-%d"),
                "Số tín hiệu": n, "Mức cảnh báo": ALERT_LEVELS.get(n, str(n)),
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
    out = pd.DataFrame(rows)
    if not out.empty:
        out = out.sort_values(["Số tín hiệu", "Mã"], ascending=[False, True]).reset_index(drop=True)
    return out, failed
