"""Nạp model xu hướng (joblib) — cache 1 lần."""
import sys
from functools import lru_cache

from ..config import MODEL_PATH


@lru_cache(maxsize=1)
def load_trend_model():
    # Model train bằng sklearn 1.6.1, chạy trên 1.9 cần shim module _loss
    try:
        import sklearn._loss._loss as _closs
        sys.modules.setdefault("_loss", _closs)
    except Exception:
        pass
    import joblib
    bundle = joblib.load(MODEL_PATH)
    return bundle["model"], bundle["features"], bundle.get("H", 20), bundle.get("UP_T", 0.05)
