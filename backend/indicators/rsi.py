"""Chỉ báo: RSI (Wilder) và mẫu hình RSI 2 đáy / phân kỳ dương."""
import numpy as np
import pandas as pd


def rsi_wilder(close, n=14):
    d = close.diff()
    au = d.clip(lower=0).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    ad = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    return 100 - 100 / (1 + au / ad)


def rsi_two_bottoms(df, r, k=3, max_age=60, min_gap=5):
    n = len(df)
    is_piv = (r == r.rolling(2 * k + 1, center=True).min())
    pos = pd.Series(np.arange(n, dtype=float), index=df.index)
    conf = pd.DataFrame({'rsi': r.where(is_piv), 'low': df['low'].where(is_piv),
                         'pos': pos.where(is_piv)}).shift(k)
    ev = conf.dropna()
    last = ev.reindex(df.index).ffill()
    prev = ev.shift(1).reindex(df.index).ffill()
    age = pos - last['pos']
    spacing = last['pos'] - prev['pos']
    hl = ((last['rsi'] > prev['rsi']) & (last['rsi'] < 50) & (age <= max_age)
          & (spacing >= min_gap) & (spacing <= max_age))
    div = hl & (last['low'] <= prev['low'])
    return pd.DataFrame({'rsi_hl': hl.astype(float), 'rsi_div': div.astype(float),
                         'rsi_piv_diff': last['rsi'] - prev['rsi'], 'rsi_piv_age': age}, index=df.index)
