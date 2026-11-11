"""Chỉ báo: đường trung bình (SMA / EMA). Nhận vào pandas Series."""


def sma(s, n):
    return s.rolling(
        window=n,
        min_periods=n
    ).mean()


def ema(s, n):
    return s.ewm(span=n, adjust=False).mean()
