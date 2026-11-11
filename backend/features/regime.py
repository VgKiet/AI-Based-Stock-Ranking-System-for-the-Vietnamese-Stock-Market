"""Feature: trạng thái xu hướng (regime) đa khung D/W/M."""
import numpy as np
import pandas as pd


REGIME = {
    (1, 1, 1): 'Tăng mạnh',
    (1, 1, 0): 'Điều chỉnh trong tăng',
    (1, 0, 1): 'Nhịp hồi sau điều chỉnh',
    (1, 0, 0): 'Điều chỉnh sâu',
    (0, 1, 1): 'Hồi mạnh / có thể đảo chiều',
    (0, 1, 0): 'Nhịp nghỉ trong hồi (yếu)',
    (0, 0, 1): 'Hồi kỹ thuật dạng V trong xu hướng giảm',
    (0, 0, 0): 'Giảm mạnh',
}
REGIME_BY_CODE = {m * 4 + w * 2 + d: name for (m, w, d), name in REGIME.items()}


def daily_state(close, ma10, ma50):
    s = pd.Series(np.nan, index=close.index)
    up10, ma_up = close > ma10, ma10 > ma50
    s[up10 & ma_up] = 2
    s[up10 & ~ma_up] = 1
    s[~up10 & ma_up & (close >= ma50)] = 0
    s[~up10 & ma_up & (close < ma50)] = -1
    s[~up10 & ~ma_up] = -2
    s[ma50.isna()] = np.nan
    return s


def htf_dir(close, ma10, ma50, m, sg):
    weak = (close < ma10) & (close < ma50) & (ma10 < ma50)
    d = ((m > sg) & ~weak).astype(float)
    d.iloc[:35] = np.nan
    return d


def label_regime(f):
    name = f['combo'].map(REGIME_BY_CODE)
    adj = (f['combo'] == 6)
    name = name.where(~(adj & (f['state_d'] == 0)), name + ' (giữ MA50, chờ tăng lại)')
    name = name.where(~(adj & (f['state_d'] == -1)), name + ' (GÃY MA50, cảnh báo)')
    return name
