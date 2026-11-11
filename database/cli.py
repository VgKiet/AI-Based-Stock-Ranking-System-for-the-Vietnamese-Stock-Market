"""
CLI quản lý kho giá. Chạy qua file gốc DB.py ở thư mục dự án:
    python DB.py stats
    python DB.py import
    python DB.py update
"""
import argparse
import os
import time as _time

from .config import DB_PATH, UNIVERSE_CSV
from .prices import db_stats, import_csv_to_db
from .universe import db_universe
from .sessions import expected_last_session
from .updater import update_prices


def _cmd_stats(_a):
    n, rows, last = db_stats()
    print(f"DB: {DB_PATH}")
    if not n:
        print("  (trống) — chạy: python DB.py import")
        return
    syms, _ = db_universe(0, 0.0)
    liq, _ = db_universe(0, 1.0)
    print(f"  {n} mã · {rows:,} dòng · phiên mới nhất {last}")
    print(f"  còn giao dịch: {len(syms)} mã · thanh khoản >= 1 tỷ/phiên: {len(liq)} mã")
    print(f"  phiên kỳ vọng đã có: {expected_last_session():%Y-%m-%d}")


def _cmd_import(a):
    path = a.csv or UNIVERSE_CSV
    if not os.path.exists(path):
        raise SystemExit(f"Không thấy file CSV: {path}")
    print(f"Nạp {path} ...")
    n = import_csv_to_db(path)
    print(f"Xong: {n:,} dòng.")
    _cmd_stats(a)


def _cmd_update(a):
    if a.symbols:
        syms = [s.strip().upper() for s in a.symbols.split(",") if s.strip()]
    else:
        syms, _ = db_universe(0, 1.0 if a.liquid else 0.0)
    if not syms:
        raise SystemExit("DB trống hoặc không có mã nào. Chạy `python DB.py import` trước (hoặc dùng --symbols).")
    print(f"Mục tiêu: có giá đến phiên {expected_last_session():%Y-%m-%d} · {len(syms)} mã trong phạm vi")
    t0 = _time.time()
    last_print = [0]

    def prog(done, total, updated):
        if done - last_print[0] >= 20 or done == total:
            last_print[0] = done
            print(f"  {done}/{total} mã đã xử lý · cập nhật được {updated}", flush=True)

    r = update_prices(syms, progress=prog, max_fail_streak=a.fail_streak, workers=a.workers, min_interval=a.interval)
    if r["todo"] == 0:
        print("Tất cả mã đã đủ phiên gần nhất — không cần cập nhật.")
    else:
        print(f"Xong trong {_time.time() - t0:.0f}s: cập nhật {r['updated']}/{r['todo']} mã"
              + (f" · {len(r['failed'])} mã lỗi" if r["failed"] else ""))
        if r["failed"]:
            print("  mã lỗi:", ", ".join(r["failed"][:40]) + (" ..." if len(r["failed"]) > 40 else ""))
        if r["aborted"]:
            print("!! DỪNG SỚM vì TradingView liên tiếp ngắt kết nối. Chờ vài phút rồi chạy lại "
                  "`python DB.py update` — chỉ các mã còn thiếu mới được kéo.")
    _cmd_stats(a)


def main():
    ap = argparse.ArgumentParser(description="Quản lý kho giá SQLite cho TopRank CK")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("stats", help="xem thống kê DB").set_defaults(fn=_cmd_stats)
    p_imp = sub.add_parser("import", help="nạp CSV vào DB")
    p_imp.add_argument("--csv", default=None, help="đường dẫn CSV (mặc định data/data_full_market.csv)")
    p_imp.set_defaults(fn=_cmd_import)
    p_up = sub.add_parser("update", help="kéo giá mới từ TradingView, chỉ phần còn thiếu")
    p_up.add_argument("--liquid", action="store_true", help="chỉ mã thanh khoản >= 1 tỷ/phiên")
    p_up.add_argument("--symbols", default=None, help="danh sách mã, cách nhau bằng dấu phẩy")
    p_up.add_argument("--workers", type=int, default=2)
    p_up.add_argument("--interval", type=float, default=0.4, help="giây giãn cách giữa các request")
    p_up.add_argument("--fail-streak", type=int, default=8, help="dừng sớm sau ngần này mã lỗi liên tiếp")
    p_up.set_defaults(fn=_cmd_update)
    a = ap.parse_args()
    a.fn(a)
