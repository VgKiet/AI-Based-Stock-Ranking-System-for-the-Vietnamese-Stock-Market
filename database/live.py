"""Lấy giá 1 mã qua DB, tự kéo thêm từ TradingView khi cần (dùng cho tab Phân tích 1 mã)."""
import pandas as pd

from .config import DB_MIN_BARS
from .prices import db_meta, db_read, db_upsert
from .tradingview import tv_fetch


def fetch_live(ticker: str, n_bars: int = 2000, hint: str = None, offline: bool = False):
    """Lấy giá qua DB: chưa có -> kéo đủ lịch sử rồi lưu; đã có -> chỉ kéo vài phiên mới rồi ghép.
    Nếu TradingView lỗi mà DB có sẵn -> dùng giá cũ trong DB. offline=True -> chỉ đọc DB, không gọi mạng."""
    t = ticker.upper().strip().split()[0]
    last, cnt, ex_db = db_meta(t)
    if offline:
        return (db_read(t, n_bars), ex_db) if cnt else (None, None)
    ex_hint = ex_db or hint
    if cnt >= DB_MIN_BARS:
        gap = max((pd.Timestamp.today().normalize() - pd.Timestamp(last)).days, 0)
        df_new, ex = tv_fetch(t, min(gap + 5, n_bars), ex_hint)
        if df_new is not None:
            db_upsert(t, ex, df_new)
        return db_read(t, n_bars), (ex or ex_db)          # TV lỗi -> vẫn trả dữ liệu cũ trong DB
    df_full, ex = tv_fetch(t, n_bars, ex_hint)
    if df_full is not None:
        db_upsert(t, ex, df_full)
        return db_read(t, n_bars), ex
    return (db_read(t, n_bars), ex_db) if cnt else (None, None)
