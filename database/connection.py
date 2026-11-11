"""Kết nối SQLite (WAL) và tạo bảng prices nếu chưa có."""
import os
import sqlite3

from .config import DB_PATH


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = sqlite3.connect(DB_PATH, timeout=60)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("""CREATE TABLE IF NOT EXISTS prices(
        symbol TEXT NOT NULL, date TEXT NOT NULL, exchange TEXT,
        open REAL, high REAL, low REAL, close REAL, volume REAL,
        PRIMARY KEY(symbol, date))""")
    return con
