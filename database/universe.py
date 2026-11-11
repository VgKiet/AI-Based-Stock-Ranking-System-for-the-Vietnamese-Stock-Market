"""Danh sách mã (universe) lấy từ DB, lọc theo thanh khoản."""
import os

import pandas as pd

from .config import DB_PATH
from .connection import get_connection


def db_universe(size: int = 0, min_value_bn: float = 0.0):
    """Danh sách mã đang còn giao dịch trong DB (có dữ liệu trong 400 ngày gần nhất của DB), sắp theo
    giá trị giao dịch trung vị giảm dần. size=0 -> tất cả. Trả (symbols, {mã: sàn})."""
    if not os.path.exists(DB_PATH):
        return [], {}
    con = get_connection()
    try:
        px = pd.read_sql_query(
            "SELECT symbol, close, volume FROM prices WHERE date >= date((SELECT MAX(date) FROM prices),'-400 day')", con)
        exs = pd.read_sql_query("SELECT symbol, MAX(exchange) AS exchange FROM prices GROUP BY symbol", con)
    finally:
        con.close()
    if px.empty:
        return [], {}
    px["v"] = px["close"] * px["volume"]
    med = px.groupby("symbol").agg(v=("v", "median"), c=("close", "median"))
    med["v"] = med["v"] * med["c"].apply(lambda c: 1.0 if c > 1000 else 1000.0) / 1e9   # tỷ đồng/phiên
    med = med[med["v"] >= min_value_bn].sort_values("v", ascending=False)
    syms = list(med.head(size).index) if size else list(med.index)
    return syms, dict(zip(exs["symbol"], exs["exchange"]))
