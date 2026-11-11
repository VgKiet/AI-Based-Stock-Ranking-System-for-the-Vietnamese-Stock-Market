"""Chạy toàn bộ backtest: đọc DB -> tạo tín hiệu -> tổng hợp -> lưu CSV."""
import pandas as pd

from .config import (
    DB_PATH, MIN_TURNOVER_VND, HORIZONS, OUTPUT_DIR,
)
from .data_loader import load_all_prices
from .signals import backtest_one_symbol
from .summary import build_summary


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 68)
    print("BACKTEST EUPHORIA CROSS-UP 0.8")
    print(f"Thanh khoản tối thiểu: {MIN_TURNOVER_VND:,.0f} VND/phiên")
    print(f"Horizon: {HORIZONS} phiên")
    print("=" * 68)

    data = load_all_prices(DB_PATH)

    all_events = []
    symbols = sorted(data["symbol"].unique())
    print(f"[INFO] Số mã trong database: {len(symbols):,}")

    for i, (symbol, group) in enumerate(data.groupby("symbol"), start=1):
        try:
            records = backtest_one_symbol(symbol, group)
            all_events.extend(records)
        except Exception as exc:
            print(f"[WARN] Bỏ qua {symbol}: {exc}")

        if i % 100 == 0 or i == len(symbols):
            print(f"[PROGRESS] {i:,}/{len(symbols):,} mã")

    if not all_events:
        print(
            "\nKhông tìm thấy tín hiệu phù hợp. "
            "Kiểm tra dữ liệu OHLCV, đơn vị giá và ngưỡng thanh khoản."
        )
        return

    events = pd.DataFrame(all_events).sort_values(
        ["signal_date", "symbol"]
    ).reset_index(drop=True)

    summary = build_summary(events)

    events_path = OUTPUT_DIR / "euphoria_events.csv"
    summary_path = OUTPUT_DIR / "euphoria_summary.csv"

    events.to_csv(events_path, index=False, encoding="utf-8-sig")
    summary.to_csv(summary_path, index=False, encoding="utf-8-sig")

    print("\n" + "=" * 68)
    print("TỔNG HỢP KẾT QUẢ")
    print("=" * 68)
    print(f"Tổng số tín hiệu: {len(events):,}")
    print(f"Số mã có tín hiệu: {events['symbol'].nunique():,}")
    print(f"Ngày tín hiệu đầu tiên: {events['signal_date'].min()}")
    print(f"Ngày tín hiệu cuối cùng: {events['signal_date'].max()}")

    if not summary.empty:
        print("\n", summary.round(2).to_string(index=False))

    print("\nĐã lưu:")
    print(f"- Chi tiết tín hiệu: {events_path}")
    print(f"- Bảng tổng hợp:     {summary_path}")
    print(
        "\nLưu ý: MFE là mức tăng tối đa nhìn lại trong H phiên, "
        "không đồng nghĩa nhà đầu tư chắc chắn bán được đúng tại mức High đó."
    )
