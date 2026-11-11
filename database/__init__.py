"""
database — Kho giá SQLite (data/prices.db) + cập nhật giá mới từ TradingView (tvDatafeed).

Chạy độc lập, không cần Streamlit hay model. backend / frontend chỉ ĐỌC từ đây.

    connection.py   kết nối SQLite
    prices.py       đọc/ghi giá, thống kê, nạp CSV
    universe.py     danh sách mã + lọc thanh khoản
    sessions.py     phiên giao dịch kỳ vọng
    tradingview.py  client TradingView + dò sàn
    updater.py      cập nhật giá hàng loạt
    live.py         lấy giá 1 mã (DB trước, TradingView sau)
    cli.py          lệnh `python DB.py ...`
"""
from .config import EXCHANGES, UNIVERSE_CSV, DB_PATH, DB_MIN_BARS
from .connection import get_connection
from .prices import db_meta, db_read, db_upsert, db_stats, import_csv_to_db, db_meta_all
from .universe import db_universe
from .sessions import expected_last_session
from .tradingview import get_tv, tv_fetch
from .updater import update_prices
from .live import fetch_live
