"""Feature: gộp nến sang khung tuần/tháng và ghép ngược về khung ngày."""
import pandas as pd


def resample_ohlcv(df, rule):
    agg = {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}
    out = df.resample(rule).agg(agg)
    last_day = pd.Series(df.index, index=df.index).resample(rule).max()
    ok = out['close'].notna()
    out = out[ok]
    out.index = pd.DatetimeIndex(last_day[ok].values, name='time').astype('datetime64[ns]')
    return out


def attach_htf(base, htf):
    left = base[[]].reset_index()
    right = htf.reset_index()
    left['time'] = left['time'].astype('datetime64[ns]')
    right['time'] = right['time'].astype('datetime64[ns]')
    merged = pd.merge_asof(left, right, on='time', direction='backward').set_index('time')
    return merged
