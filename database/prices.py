"""Đọc / ghi bảng giá: meta từng mã, đọc nến, upsert, thống kê, nạp CSV."""
import os

import pandas as pd

from .config import DB_PATH
from .connection import get_connection


def db_meta(symbol: str):
    """(ngày cuối, số dòng, sàn) của 1 mã; (None, 0, None) nếu chưa có."""
    con = get_connection()
    try:
        r = con.execute("SELECT MAX(date), COUNT(*), MAX(exchange) FROM prices WHERE symbol=?", (symbol,)).fetchone()
    finally:
        con.close()
    return (r[0], r[1], r[2]) if r and r[1] else (None, 0, None)


def db_read(symbol: str, n_bars: int = 2000):
    con = get_connection()
    try:
        df = pd.read_sql_query(
            "SELECT date AS datetime, open, high, low, close, volume FROM prices "
            "WHERE symbol=? ORDER BY date DESC LIMIT ?", con, params=(symbol, int(n_bars)))
    finally:
        con.close()
    if df.empty:
        return None
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df.sort_values("datetime").reset_index(drop=True)


def db_upsert(symbol: str, exchange: str, df_raw: pd.DataFrame):
    d = df_raw.copy()
    if "datetime" not in d.columns:
        d = d.reset_index()
        if "datetime" not in d.columns and "index" in d.columns:
            d = d.rename(columns={"index": "datetime"})
    d["date"] = pd.to_datetime(d["datetime"]).dt.normalize().dt.strftime("%Y-%m-%d")
    d = d.drop_duplicates("date", keep="last")
    rows = [(symbol, r.date, exchange, float(r.open), float(r.high), float(r.low), float(r.close), float(r.volume))
            for r in d.itertuples()]
    con = get_connection()
    try:
        with con:
            con.executemany("INSERT OR REPLACE INTO prices VALUES (?,?,?,?,?,?,?,?)", rows)
    finally:
        con.close()


def db_stats():
    """(số mã, số dòng, ngày mới nhất) hoặc (0, 0, None)."""
    if not os.path.exists(DB_PATH):
        return 0, 0, None
    con = get_connection()
    try:
        r = con.execute("SELECT COUNT(DISTINCT symbol), COUNT(*), MAX(date) FROM prices").fetchone()
    finally:
        con.close()
    return (r[0] or 0, r[1] or 0, r[2])


def import_csv_to_db(csv_path: str) -> int:
    """Nạp data_full_market.csv (date,symbol,open,high,low,close,volume,exchange) vào DB. Trả số dòng đã nạp."""
    raw = pd.read_csv(csv_path, usecols=["date", "symbol", "open", "high", "low", "close", "volume", "exchange"])
    raw["date"] = pd.to_datetime(raw["date"]).dt.normalize().dt.strftime("%Y-%m-%d")
    raw = raw[(raw["close"] > 0) & (raw["low"] > 0) & (raw["high"] >= raw["low"]) & (raw["volume"] > 0)]
    raw = raw.drop_duplicates(["symbol", "date"], keep="last")
    raw["symbol"] = raw["symbol"].astype(str).str.upper()
    raw["exchange"] = raw["exchange"].astype(str).str.upper().replace({"HSX": "HOSE"})
    cols = ["symbol", "date", "exchange", "open", "high", "low", "close", "volume"]
    con = get_connection()
    n = 0
    try:
        with con:
            for i in range(0, len(raw), 100_000):
                chunk = raw.iloc[i:i + 100_000][cols]
                con.executemany("INSERT OR REPLACE INTO prices VALUES (?,?,?,?,?,?,?,?)",
                                list(chunk.itertuples(index=False, name=None)))
                n += len(chunk)
    finally:
        con.close()
    return n


def db_meta_all():
    """{symbol: (ngày cuối, số dòng, sàn)} cho toàn DB — 1 câu truy vấn."""
    if not os.path.exists(DB_PATH):
        return {}
    con = get_connection()
    try:
        rows = con.execute("SELECT symbol, MAX(date), COUNT(*), MAX(exchange) FROM prices GROUP BY symbol").fetchall()
    finally:
        con.close()
    return {r[0]: (r[1], r[2], r[3]) for r in rows}
