"""
Chỉ báo hưng phấn thị trường trong đoạn [-1, 1]
  +1: hưng phấn cực độ | 0: trung tính | -1: bi quan / hoảng loạn cực độ
"""
import numpy as np
import pandas as pd

from .rsi import rsi_wilder

EUPHORIA_W = dict(stretch=0.30, rsi=0.25, range=0.20, vol=0.15, roc=0.10)
EUPHORIA_HI, EUPHORIA_LO = 0.8, -0.8
EUPHORIA_LABELS = dict(stretch="Độ giãn giá so với MA50", rsi="RSI", range="Vị trí trong vùng giá 120 phiên",
                       vol="Áp lực khối lượng", roc="Động lượng ROC")


def euphoria_index(df, ma_len=50, rsi_len=14, range_len=120, vol_len=20, roc_len=20, smooth=5, weights=None):
    """df: index thời gian, cột open/high/low/close/volume. Trả DataFrame 5 thành phần + cột 'euphoria' trong [-1, 1]."""
    w = {**EUPHORIA_W, **(weights or {})}
    c, h, l = df['close'], df['high'], df['low']
    v = df['volume'] if 'volume' in df.columns else pd.Series(0.0, index=df.index)

    sd = c.rolling(ma_len).std(ddof=0).replace(0, np.nan)
    s_stretch = np.tanh(((c - c.rolling(ma_len).mean()) / sd) / 2.0)
    s_rsi = ((rsi_wilder(c, rsi_len) - 50.0) / 30.0).clip(-1, 1)
    hh, ll = h.rolling(range_len).max(), l.rolling(range_len).min()
    s_range = 2.0 * (c - ll) / (hh - ll).replace(0, np.nan) - 1.0
    d = c.diff()
    up = v.where(d > 0, 0.0).rolling(vol_len).sum()
    dn = v.where(d < 0, 0.0).rolling(vol_len).sum()
    s_vol = (up - dn) / (up + dn).replace(0, np.nan)
    roc = c.pct_change(roc_len) * 100
    roc_sd = roc.rolling(range_len).std(ddof=0).replace(0, np.nan)
    s_roc = np.tanh((roc / roc_sd) / 2.0)

    comps = pd.DataFrame({'stretch': s_stretch, 'rsi': s_rsi, 'range': s_range, 'vol': s_vol, 'roc': s_roc})
    wts = pd.Series(w)[comps.columns]
    raw = (comps * wts).sum(axis=1, skipna=False) / wts.sum()
    comps['euphoria'] = raw.ewm(span=smooth, adjust=False).mean().clip(-1, 1)
    return comps


def euphoria_zone(x, hi=EUPHORIA_HI, lo=EUPHORIA_LO):
    """Trả (nhãn, màu) theo mức hưng phấn."""
    if x is None or pd.isna(x):
        return "N/A", "#9aa3b2"
    if x >= hi:   return "Hưng phấn quá mức", "#0b8f6a"
    if x >= 0.4:  return "Hưng phấn", "#26a69a"
    if x > -0.4:  return "Trung tính", "#6b7280"
    if x > lo:    return "Bi quan", "#ef5350"
    return "Bi quan / hoảng loạn cực độ", "#c62828"
