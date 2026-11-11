"""Mỗi chỉ báo một file. Thêm chỉ báo mới: tạo file mới ở đây rồi export thêm vào dưới."""
from .moving_average import sma, ema
from .macd import macd
from .rsi import rsi_wilder, rsi_two_bottoms
from .adx import adx
from .regression_channel import reg_channel
from .euphoria import (
    EUPHORIA_W, EUPHORIA_HI, EUPHORIA_LO, EUPHORIA_LABELS,
    euphoria_index, euphoria_zone,
)
