"""backend/preprocess.py — Chuẩn hoá dữ liệu giá thô (từ DB / TradingView) về đúng dạng lúc train."""
import pandas as pd


def _normalize_vn(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "datetime" not in df.columns:
        df = df.reset_index()
    if "datetime" not in df.columns and "index" in df.columns:
        df = df.rename(columns={"index": "datetime"})
    for c in ["open", "high", "low", "close"]:
        if c in df.columns and len(df) and float(df[c].median()) > 1000:
            df[c] = df[c] / 1000
    return df


def to_daily_indexed(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Chuẩn hoá về dạng train: index time, cột open/high/low/close/volume."""
    df = _normalize_vn(df_raw)
    df["time"] = pd.to_datetime(df["datetime"])
    df = df.set_index("time").sort_index()
    keep = [c for c in ["open", "high", "low", "close", "volume"] if c in df.columns]
    return df[keep]
