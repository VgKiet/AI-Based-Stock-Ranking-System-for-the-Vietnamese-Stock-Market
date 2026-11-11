"""SEPA 3 — Chuỗi đỉnh cao hơn, đáy cao hơn."""
import numpy as np

from .config import PIVOT_ORDER, PIVOT_LOOKBACK, PIVOT_COUNT


def find_pivots(series, order, kind):
    """Giá trị các đỉnh (kind='high') hoặc đáy (kind='low'), theo thứ tự thời gian.
    Đỉnh/đáy chỉ được xác nhận khi đã có `order` phiên sau nó."""
    win = 2 * order + 1
    roll = series.rolling(win, center=True)
    ext = roll.max() if kind == "high" else roll.min()
    mask = (series == ext) & ext.notna()
    vals = series[mask]
    # bỏ các điểm liền kề trùng giá (vùng đi ngang)
    return vals[vals.diff().fillna(1) != 0]


def check(df):
    d = df.tail(PIVOT_LOOKBACK + PIVOT_ORDER)
    highs = find_pivots(d["high"] if "high" in d else d["close"], PIVOT_ORDER, "high").tail(PIVOT_COUNT)
    lows = find_pivots(d["low"] if "low" in d else d["close"], PIVOT_ORDER, "low").tail(PIVOT_COUNT)
    if len(highs) < PIVOT_COUNT or len(lows) < PIVOT_COUNT:
        return {"ok": False, "value": f"thiếu đỉnh/đáy ({len(highs)}đ/{len(lows)}đáy)"}
    hh = bool(np.all(np.diff(highs.values) > 0))
    hl = bool(np.all(np.diff(lows.values) > 0))
    return {"ok": hh and hl, "value": f"đỉnh {'↑' if hh else '✗'} · đáy {'↑' if hl else '✗'}"}
