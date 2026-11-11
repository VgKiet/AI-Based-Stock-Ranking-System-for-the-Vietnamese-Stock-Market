"""Cập nhật giá mới từ TradingView vào DB (nhẹ nhàng: ít luồng, giãn cách request, ngắt sớm khi lỗi liên tiếp)."""
import logging
import threading
import time as _time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from .prices import db_meta_all, db_upsert
from .sessions import expected_last_session
from .tradingview import tv_fetch


def update_prices(symbols, progress=None, max_fail_streak: int = 8, workers: int = 2, min_interval: float = 0.4):
    """Cập nhật GIÁ MỚI vào DB, nhẹ nhàng với TradingView: ít luồng, giãn cách request, bỏ qua mã đã đủ phiên,
    chỉ kéo phần còn thiếu, và NGẮT SỚM nếu liên tiếp bị ngắt kết nối.
    progress(done, total, updated) là callback tuỳ chọn. Trả dict thống kê."""
    meta = db_meta_all()
    target = expected_last_session()
    today = pd.Timestamp.today().normalize()
    todo = [c for c in symbols if c not in meta or pd.Timestamp(meta[c][0]) < target]
    stats = {"total": len(symbols), "todo": len(todo), "updated": 0, "failed": [], "aborted": False,
             "target": target.strftime("%Y-%m-%d")}
    if not todo:
        return stats
    logging.getLogger("tvDatafeed.main").setLevel(logging.CRITICAL)     # tắt spam log lỗi của tvDatafeed
    lock, state = threading.Lock(), {"streak": 0, "stop": False, "last": 0.0, "done": 0}

    def _one(code):
        if state["stop"]:
            return
        with lock:                                        # giãn cách giữa các request
            wait = min_interval - (_time.time() - state["last"])
            state["last"] = _time.time() + max(wait, 0)
        if wait > 0:
            _time.sleep(wait)
        last, cnt, ex = meta.get(code, (None, 0, None))
        if cnt >= 1:                                      # đã có lịch sử -> chỉ kéo phần thiếu
            n_new = min((today - pd.Timestamp(last)).days + 5, 1500)
            df, ex2 = tv_fetch(code, n_new, ex, strict=bool(ex))
        else:                                             # mã mới -> tải đủ lịch sử
            df, ex2 = tv_fetch(code, 1500, None)
        with lock:
            state["done"] += 1
            if df is not None:
                db_upsert(code, ex2, df)
                stats["updated"] += 1
                state["streak"] = 0
            else:
                stats["failed"].append(code)
                state["streak"] += 1
                if state["streak"] >= max_fail_streak:
                    state["stop"] = True
            d, u = state["done"], stats["updated"]
        if df is None:
            _time.sleep(2.0)                              # lỗi -> nghỉ thêm trước mã kế tiếp
        if progress is not None:
            progress(d, len(todo), u)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(_one, todo))
    stats["aborted"] = state["stop"]
    return stats
