"""Tạo sự kiện Euphoria cắt lên ngưỡng và tính MFE cho từng mã."""
import numpy as np

from backend import euphoria_index, to_daily_indexed

from .config import MIN_TURNOVER_VND, EUPHORIA_THRESHOLD, HORIZONS


# ============================================================
# CHUẨN HÓA ĐƠN VỊ VÀ TÍNH THANH KHOẢN
# ============================================================
def prepare_symbol_data(group):
    group = group.sort_values("date").copy()

    # BE.to_daily_indexed() đang chuẩn hóa giá VND về nghìn đồng
    # nếu median giá > 1000. Ta dùng cùng quy ước để tính turnover.
    raw_price_median = group["close"].median()

    if raw_price_median > 1000:
        # Giá trong DB là VND/cổ phiếu.
        group["turnover_vnd"] = group["close"] * group["volume"]
    else:
        # Giá trong DB là nghìn VND/cổ phiếu.
        group["turnover_vnd"] = group["close"] * 1000.0 * group["volume"]

    raw = group.rename(columns={"date": "datetime"})[
        ["datetime", "open", "high", "low", "close", "volume"]
    ].copy()

    daily = to_daily_indexed(raw)
    daily = daily[~daily.index.duplicated(keep="last")].sort_index()

    # Giữ turnover theo đúng thứ tự/index của daily.
    turnover = group.set_index("date")["turnover_vnd"]
    turnover = turnover[~turnover.index.duplicated(keep="last")]
    daily["turnover_vnd"] = turnover.reindex(daily.index)

    return daily


# ============================================================
# TẠO SỰ KIỆN EUPHORIA CROSS-UP VÀ TÍNH MFE
# ============================================================
def backtest_one_symbol(symbol, group):
    daily = prepare_symbol_data(group)

    # Euphoria dùng nguyên hàm trong BE.py, không viết lại công thức.
    eu = euphoria_index(daily)
    daily["euphoria"] = eu["euphoria"]

    previous = daily["euphoria"].shift(1)

    cross_up = (
        previous.lt(EUPHORIA_THRESHOLD)
        & daily["euphoria"].ge(EUPHORIA_THRESHOLD)
    )

    # Lọc thanh khoản ngay tại phiên phát tín hiệu.
    liquid = daily["turnover_vnd"].ge(MIN_TURNOVER_VND)

    signal_rows = daily.loc[cross_up & liquid].copy()
    if signal_rows.empty:
        return []

    records = []
    dates = daily.index
    high_values = daily["high"].to_numpy()
    close_values = daily["close"].to_numpy()

    for signal_date, row in signal_rows.iterrows():
        pos = dates.get_loc(signal_date)
        entry_close = float(row["close"])

        record = {
            "symbol": symbol,
            "signal_date": signal_date.strftime("%Y-%m-%d"),
            "euphoria_previous": float(previous.loc[signal_date]),
            "euphoria_signal": float(row["euphoria"]),
            "close_signal": entry_close,
            "turnover_vnd": float(row["turnover_vnd"]),
        }

        for horizon in HORIZONS:
            start = pos + 1
            end = pos + 1 + horizon

            # Chỉ đánh giá khi có đủ H phiên sau ngày tín hiệu.
            if end > len(daily):
                record[f"mfe_{horizon}d_pct"] = np.nan
                record[f"max_high_{horizon}d"] = np.nan
                record[f"max_high_date_{horizon}d"] = None
                continue

            future_highs = high_values[start:end]
            future_dates = dates[start:end]

            max_idx = int(np.nanargmax(future_highs))
            max_high = float(future_highs[max_idx])

            record[f"mfe_{horizon}d_pct"] = (
                max_high / entry_close - 1.0
            ) * 100.0
            record[f"max_high_{horizon}d"] = max_high
            record[f"max_high_date_{horizon}d"] = (
                future_dates[max_idx].strftime("%Y-%m-%d")
            )

        records.append(record)

    return records
