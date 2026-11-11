"""Kết nối TradingView (tvDatafeed): client dùng chung + dò sàn có retry."""
import os
import threading
import time as _time

from .config import EXCHANGES


_TV = None
_TV_LOCK = threading.Lock()


def get_tv():
    """TvDatafeed dùng chung (đăng nhập nếu có TV_USER/TV_PASS)."""
    global _TV
    with _TV_LOCK:
        if _TV is None:
            from tvDatafeed import TvDatafeed
            u, pw = os.environ.get("TV_USER"), os.environ.get("TV_PASS")
            _TV = TvDatafeed(u, pw) if (u and pw) else TvDatafeed()
        return _TV


def tv_fetch(ticker: str, n_bars: int, hint: str = None, strict: bool = False):
    """Gọi TradingView (dò sàn, có retry). Trả (df_raw | None, exchange | None)."""
    from tvDatafeed import Interval
    tv = get_tv()
    order = ([hint] if hint in EXCHANGES else []) + [e for e in EXCHANGES if e != hint]
    if strict and hint in EXCHANGES:
        order = [hint]                            # biết chắc sàn -> không dò sàn khác (giảm số request)
    for exchange in order:
        tries = (2 if strict else 3) if exchange == hint else 1
        for k in range(tries):
            try:
                df = tv.get_hist(symbol=ticker, exchange=exchange,
                                 interval=Interval.in_daily, n_bars=n_bars)
                if df is not None and not df.empty:
                    return df, exchange
            except Exception:
                pass
            if k < tries - 1:
                _time.sleep(0.8 * (k + 1))
    return None, None
