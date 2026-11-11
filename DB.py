"""
DB.py — Kho giá SQLite (data/prices.db) + cập nhật giá mới từ TradingView (tvDatafeed).

File này CHẠY ĐỘC LẬP, không cần Streamlit, không cần model. UI.py / BE.py chỉ ĐỌC từ DB này.

Cách dùng (trong thư mục dự án, đã bật venv):
    python DB.py stats                       # xem DB đang có gì
    python DB.py import                      # nạp data/data_full_market.csv vào DB (làm 1 lần)
    python DB.py import --csv đường/dẫn.csv
    python DB.py update                      # chỉ kéo các phiên CÒN THIẾU của mọi mã trong DB
    python DB.py update --liquid             # chỉ các mã thanh khoản >= 1 tỷ/phiên (nhanh hơn)
    python DB.py update --symbols FPT,ACB    # chỉ định mã (mã chưa có trong DB sẽ tải đủ lịch sử)

Gợi ý: chạy `update` sau 15:00 mỗi ngày giao dịch. Mã đã đủ phiên gần nhất sẽ được bỏ qua.
Đăng nhập TradingView (ít bị chặn hơn): đặt biến môi trường TV_USER và TV_PASS trước khi chạy.
"""
from database.cli import main

if __name__ == "__main__":
    main()
