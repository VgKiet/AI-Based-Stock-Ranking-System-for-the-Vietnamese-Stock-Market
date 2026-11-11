"""Bảng tổng hợp thống kê MFE theo horizon."""
import pandas as pd

from .config import HORIZONS


def build_summary(events):
    if events.empty:
        return pd.DataFrame()

    rows = []
    for horizon in HORIZONS:
        col = f"mfe_{horizon}d_pct"
        values = events[col].dropna()

        if values.empty:
            continue

        rows.append({
            "Horizon": f"{horizon} phiên",
            "Số tín hiệu đủ dữ liệu": int(values.count()),
            "MFE trung bình (%)": values.mean(),
            "MFE trung vị (%)": values.median(),
            "MFE lớn nhất (%)": values.max(),
            "MFE nhỏ nhất (%)": values.min(),
            "Tỷ lệ có thể tăng > 0% (%)": (values > 0).mean() * 100,
            "Tỷ lệ đạt > 3% (%)": (values >= 3).mean() * 100,
            "Tỷ lệ đạt > 5% (%)": (values >= 5).mean() * 100,
            "Tỷ lệ đạt > 10% (%)": (values >= 10).mean() * 100,
        })

    return pd.DataFrame(rows)
