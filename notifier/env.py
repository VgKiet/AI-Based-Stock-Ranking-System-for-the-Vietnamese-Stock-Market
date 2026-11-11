"""Đọc file .env (không cần thư viện ngoài)."""
import os

from paths import ENV_PATH


def load_env(path: str = None):
    """Đọc file .env (KEY=VALUE, bỏ qua dòng trống và dòng bắt đầu bằng #). Không ghi đè biến đã có sẵn."""
    path = path or str(ENV_PATH)
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip().removeprefix("export "), v.strip().strip('"').strip("'")
            os.environ.setdefault(k.strip(), v)
