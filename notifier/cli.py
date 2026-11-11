"""CLI gửi Telegram — chạy qua file gốc telegram_notify.py."""
import argparse
import os
import sys
from datetime import datetime

from .env import load_env
from .messages import build_rank_message, build_liquid_message, split_message
from .telegram_api import send_telegram, find_chat_ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["rank", "liquid"], default="rank")
    ap.add_argument("--top", type=int, default=50)
    ap.add_argument("--min-value", type=float, default=1.0, help="thanh khoản tối thiểu, tỷ đồng/phiên")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--get-chat-id", action="store_true", help="dò chat ID rồi thoát")
    a = ap.parse_args()
    load_env()

    if a.get_chat_id:
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            sys.exit("Thiếu TELEGRAM_BOT_TOKEN trong .env.")
        return find_chat_ids(token)

    msg = (build_rank_message if a.mode == "rank" else build_liquid_message)(a.top, a.min_value)
    parts = split_message(msg)

    if a.dry_run:
        for p in parts:
            print(p, "\n" + "-" * 40)
        return
    token, chat_id = os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        sys.exit("Thiếu TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID (đặt trong file .env cạnh telegram_notify.py).")
    for p in parts:
        send_telegram(token, chat_id, p)
    print(f"✅ Đã gửi {len(parts)} tin lúc {datetime.now():%H:%M %d/%m/%Y}")
