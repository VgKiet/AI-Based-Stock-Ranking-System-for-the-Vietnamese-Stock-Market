"""Gọi Telegram Bot API: gửi tin và dò chat ID."""
import sys

import requests


def send_telegram(token: str, chat_id: str, text: str):
    r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                      data={"chat_id": chat_id, "text": text, "parse_mode": "HTML",
                            "disable_web_page_preview": True}, timeout=30)
    if not r.ok:
        raise RuntimeError(f"Telegram lỗi {r.status_code}: {r.text}")


def find_chat_ids(token: str):
    """Gọi getUpdates, in ra các chat đã nhắn cho bot (chat ID đúng để điền vào .env)."""
    r = requests.get(f"https://api.telegram.org/bot{token}/getUpdates", timeout=30)
    if not r.ok:
        sys.exit(f"Telegram lỗi {r.status_code}: {r.text}\n-> Kiểm tra lại TELEGRAM_BOT_TOKEN trong .env.")
    seen = {}
    for u in r.json().get("result", []):
        for key in ("message", "edited_message", "channel_post", "my_chat_member"):
            chat = (u.get(key) or {}).get("chat")
            if chat:
                seen[chat["id"]] = chat
    if not seen:
        sys.exit("Chưa thấy chat nào. Mở chat với bot của bạn, gõ 'hi' rồi chạy lại lệnh này.")
    print("Các chat đã nhắn cho bot (điền số 'id' vào TELEGRAM_CHAT_ID):")
    for cid, c in seen.items():
        name = c.get("title") or " ".join(filter(None, [c.get("first_name"), c.get("last_name")])) or c.get("username", "")
        print(f"  id = {cid}   ({c.get('type')}) {name}")
