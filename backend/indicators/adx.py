"""Chỉ báo: ADX (độ mạnh xu hướng)."""
import numpy as np
import pandas as pd


def adx(df, n=14):
    up, dn = df['high'].diff(), -df['low'].diff()
    plus = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), index=df.index)
    minus = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), index=df.index)
    tr = pd.concat([df['high'] - df['low'],
                    (df['high'] - df['close'].shift()).abs(),
                    (df['low'] - df['close'].shift()).abs()], axis=1).max(axis=1)
    w = dict(alpha=1 / n, adjust=False, min_periods=n)
    atr = tr.ewm(**w).mean()
    pdi = 100 * plus.ewm(**w).mean() / atr
    mdi = 100 * minus.ewm(**w).mean() / atr
    dx = 100 * (pdi - mdi).abs() / (pdi + mdi)
    return dx.ewm(**w).mean()
