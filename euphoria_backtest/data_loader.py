"""Đọc toàn bộ giá từ SQLite (tự dò bảng/cột OHLCV)."""
import sqlite3

import pandas as pd


ALIASES = {
    "symbol": ["symbol", "ticker", "code", "stock_code", "symbol_code"],
    "date": ["date", "datetime", "time", "trading_date", " 거래일"],
    "open": ["open", "o"],
    "high": ["high", "h"],
    "low": ["low", "l"],
    "close": ["close", "c", "adj_close", "close_price"],
    "volume": ["volume", "vol", "v", "trading_volume"],
}


def quote_identifier(name):
    return '"' + str(name).replace('"', '""') + '"'


def find_price_table(conn):
    tables = pd.read_sql_query(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """,
        conn,
    )["name"].tolist()

    candidates = []

    for table in tables:
        info = pd.read_sql_query(
            f"PRAGMA table_info({quote_identifier(table)})", conn
        )
        columns = {str(c).lower(): str(c) for c in info["name"]}

        mapping = {}
        for target, names in ALIASES.items():
            for alias in names:
                if alias.lower() in columns:
                    mapping[target] = columns[alias.lower()]
                    break

        required = {"symbol", "date", "open", "high", "low", "close", "volume"}
        if required.issubset(mapping):
            candidates.append((table, mapping))

    if not candidates:
        raise RuntimeError(
            "Không tìm thấy bảng OHLCV phù hợp trong SQLite. "
            "Cần các cột symbol/ticker, date, open, high, low, close, volume."
        )

    # Ưu tiên bảng có tên prices, sau đó mới đến bảng phù hợp đầu tiên.
    candidates.sort(key=lambda x: (x[0].lower() != "prices", x[0].lower()))
    return candidates[0]


def load_all_prices(db_path):
    if not db_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy database: {db_path}\n"
            "Hãy sửa DB_PATH trong backtest.py cho đúng vị trí prices.db."
        )

    conn = sqlite3.connect(str(db_path))
    try:
        table, cols = find_price_table(conn)
        selected = [
            f"{quote_identifier(cols[k])} AS {quote_identifier(k)}"
            for k in ("symbol", "date", "open", "high", "low", "close", "volume")
        ]
        query = (
            f"SELECT {', '.join(selected)} "
            f"FROM {quote_identifier(table)}"
        )
        data = pd.read_sql_query(query, conn)
    finally:
        conn.close()

    print(f"[INFO] Đọc bảng SQLite: {table}")
    print(f"[INFO] Số dòng dữ liệu: {len(data):,}")

    data["symbol"] = data["symbol"].astype(str).str.strip().str.upper()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")

    for col in ("open", "high", "low", "close", "volume"):
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna(
        subset=["symbol", "date", "open", "high", "low", "close", "volume"]
    )
    data = data[data["volume"] > 0]
    data = data.sort_values(["symbol", "date"])
    data = data.drop_duplicates(["symbol", "date"], keep="last")

    return data
