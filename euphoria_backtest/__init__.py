"""
euphoria_backtest — Kiểm định tín hiệu Euphoria cắt lên 0.8 trên dữ liệu SQLite hiện có.

Quy ước:
- Tín hiệu: Euphoria[t-1] < 0.8 và Euphoria[t] >= 0.8.
- Thanh khoản phiên tín hiệu >= 1 tỷ VND.
- Giá vào tham chiếu: Close tại ngày tín hiệu.
- MFE: High cao nhất trong 5/10/20 phiên SAU ngày tín hiệu.
- Không dùng dữ liệu tương lai để xác định tín hiệu.
- Chỉ tính MFE cho horizon có đủ số phiên tương lai.

Chạy:  python backtest.py        (sửa ngưỡng/horizon trong euphoria_backtest/config.py)
"""
