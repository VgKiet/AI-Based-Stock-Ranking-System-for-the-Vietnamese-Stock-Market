"""Dự đoán xu hướng 1 mã: tính feature rồi predict_proba (Giảm / Đi ngang / Tăng sau H phiên)."""
import numpy as np
import pandas as pd

from ..features import build_features
from .model_loader import load_trend_model


def predict_trend(df_daily: pd.DataFrame):
    """Tính feature đúng train + predict_proba. Trả dict kết quả dòng cuối."""
    model, features, H, UP_T = load_trend_model()
    feats = build_features(df_daily)
    if feats.empty:
        raise ValueError("Không tính được feature (quá ít nến).")
    last = feats.iloc[-1]
    x = feats[features].iloc[[-1]]
    p = model.predict_proba(x)[0]  # [P(giảm), P(ngang), P(tăng)]
    pred = int(np.argmax(p))
    return {
        "H": H, "UP_T": UP_T, "features": feats,
        "p_down": float(p[0]), "p_flat": float(p[1]), "p_up": float(p[2]),
        "pred": pred, "pred_name": ["Giảm", "Đi ngang", "Tăng"][pred],
        "regime": str(last.get("regime", "—")),
        "D": last.get("dir_d"), "W": last.get("dir_w"), "M": last.get("dir_m"),
        "rsi_d": last.get("rsi_d"), "adx_d": last.get("adx_d"),
        "chan_d": last.get("chan_pos_d"), "chan_w": last.get("chan_pos_w"), "chan_m": last.get("chan_pos_m"),
        "rsi_hl": last.get("rsi_hl_d"), "rsi_div": last.get("rsi_div_d"),
        "break50": last.get("break50_d"), "break50_strong": last.get("break50_strong_d"),
        "state_d": last.get("state_d"), "sideways": last.get("sideways"),
        "last_time": feats.index[-1],
    }
