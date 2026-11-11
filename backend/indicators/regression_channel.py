"""Chỉ báo: kênh hồi quy tuyến tính (log giá) — vị trí trong kênh, độ dốc, độ rộng."""
import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view

from ..config import CHAN_K


def reg_channel(close, n, k=CHAN_K):
    cols = ['chan_pos', 'chan_slope', 'chan_width', 'chan_out']
    res = np.full((len(close), 4), np.nan)
    y = np.log(close.values.astype(float))
    if len(y) >= n:
        w = sliding_window_view(y, n)
        x = np.arange(n) - (n - 1) / 2
        slope = (w * x).sum(1) / (x ** 2).sum()
        mean = w.mean(1)
        fit = mean[:, None] + slope[:, None] * x
        sd = np.sqrt(((w - fit) ** 2).mean(1))
        sd = np.where(sd == 0, np.nan, sd)
        last_fit = mean + slope * x[-1]
        pos = (w[:, -1] - (last_fit - k * sd)) / (2 * k * sd)
        res[n - 1:, 0] = pos
        res[n - 1:, 1] = slope * n
        res[n - 1:, 2] = 2 * k * sd
        res[n - 1:, 3] = np.where(pos < 0, -1, np.where(pos > 1, 1, 0))
        res[n - 1:, 3] = np.where(np.isnan(pos), np.nan, res[n - 1:, 3])
    return pd.DataFrame(res, index=close.index, columns=cols)
