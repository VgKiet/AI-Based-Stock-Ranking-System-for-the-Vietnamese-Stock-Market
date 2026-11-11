"""SEPA 2 — MA(200) hướng lên ít nhất 1 tháng."""
from ...indicators import sma
from .config import MA_LONG, MA200_RISING_SESSIONS


def check(df):
    ma = sma(df["close"], MA_LONG)
    now, before = float(ma.iloc[-1]), float(ma.iloc[-1 - MA200_RISING_SESSIONS])
    chg = (now / before - 1) * 100
    return {"ok": bool(now > before), "value": f"{chg:+.2f}%"}
