"""
Feature pipeline — COPY ĐÚNG từ notebook train (train/pred_stock_vn_*.ipynb).
Đừng đổi logic ở đây nếu chưa train lại model, vì model dùng đúng các cột này.
"""
import pandas as pd

from ..config import CHAN_N
from ..indicators import sma, macd, rsi_wilder, adx, reg_channel, rsi_two_bottoms
from .regime import daily_state, htf_dir, label_regime
from .timeframe import resample_ohlcv, attach_htf


def tf_features(df, n_chan):
    c = df['close']
    ma10, ma50 = sma(c, 10), sma(c, 50)
    m, sg, h = macd(c)
    f = pd.DataFrame(index=df.index)
    f['dir'] = htf_dir(c, ma10, ma50, m, sg)
    f['macd_hist'] = h / c
    f['dist_ma10'] = c / ma10 - 1
    f['dist_ma50'] = c / ma50 - 1
    f['ma_gap'] = ma10 / ma50 - 1
    f['rsi'] = rsi_wilder(c)
    return pd.concat([f, reg_channel(c, n_chan)], axis=1)


def daily_features(df):
    f = tf_features(df, CHAN_N['D'])
    c, v = df['close'], df['volume']
    ma10, ma50 = sma(c, 10), sma(c, 50)
    stt = daily_state(c, ma10, ma50)
    f['state'] = stt
    f['dir'] = (stt >= 1).astype(float).where(stt.notna())
    f['adx'] = adx(df)
    f['vol_ratio'] = v / sma(v, 20)
    f['ma_gap_small'] = (f['ma_gap'].abs() < 0.02).astype(float)
    f['break50'] = (stt == -1).astype(float)
    f['break50_strong'] = ((stt == -1) & ((f['vol_ratio'] > 1) | (f['dist_ma50'] < -0.02))).astype(float)
    f['below50_3d'] = (c < ma50).astype(float).rolling(3).sum()
    f['ret_5'] = c.pct_change(5)
    f['ret_20'] = c.pct_change(20)
    return pd.concat([f, rsi_two_bottoms(df, f['rsi'])], axis=1)


def build_features(df_daily):
    d = daily_features(df_daily).add_suffix('_d')
    w = tf_features(resample_ohlcv(df_daily, 'W-FRI'), CHAN_N['W']).add_suffix('_w')
    m = tf_features(resample_ohlcv(df_daily, 'MS'), CHAN_N['M']).add_suffix('_m')
    out = pd.concat([d, attach_htf(d, w), attach_htf(d, m)], axis=1)
    out['combo'] = out['dir_m'] * 4 + out['dir_w'] * 2 + out['dir_d']
    out['regime'] = label_regime(out)
    out['sideways'] = (out['adx_d'] < 20).astype(float).where(out['adx_d'].notna())
    return out
