# TopRank CK

Hệ thống nhận diện xu hướng và xếp hạng cổ phiếu Việt Nam. Dùng mô hình học máy dự đoán xu hướng **Tăng / Đi ngang / Giảm** sau H phiên, kết hợp bộ lọc **SEPA**, cảnh báo **break out thất bại**, backtest chỉ báo **Euphoria** và gửi kết quả qua **Telegram**.

> ⚠️ **Lưu ý:** Dự án phục vụ học tập và nghiên cứu, không phải khuyến nghị đầu tư. Mọi quyết định mua bán do bạn tự chịu trách nhiệm.

---

## 1. Tính năng

| Tính năng | Mô tả |
|---|---|
| 🏆 Top xác suất tăng | Quét toàn thị trường, xếp hạng theo xác suất tăng của model, lọc thanh khoản (Penny filter) và loại các mã không mong muốn |
| 📈 Phân tích 1 mã | Biểu đồ giá, xác suất Tăng/Đi ngang/Giảm, chỉ báo hưng phấn Euphoria, trạng thái regime D/W/M, bảng feature |
| 🔎 Lọc SEPA | Quét thị trường theo các điều kiện SEPA: MA, MA200 dốc lên, đỉnh/đáy cao dần, khối lượng, khoảng cách tới đáy/đỉnh |
| ⚠️ Cảnh báo thất bại | Phát hiện break out thất bại: giá dưới MA20, đáy thấp dần, phân kỳ khối lượng |
| 🧪 Backtest | Backtest tín hiệu Euphoria cắt lên 0.8 |
| 🗄️ Kho giá | Lưu giá trong SQLite, cập nhật phiên mới từ TradingView |
| 📨 Telegram | Gửi danh sách top mã qua bot Telegram |

---

## 2. Cài đặt

### Yêu cầu

- Python 3.10+ (khuyến nghị dùng môi trường ảo `venv`)
- Git (để cài `tvdatafeed` từ GitHub)

### Các bước

```bash
# 1. Tạo và bật môi trường ảo
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # macOS / Linux

# 2. Cài thư viện
pip install -r requirements.txt

# 3. Tạo file cấu hình
copy .env.example .env           # Windows
# cp .env.example .env           # macOS / Linux
```

> Trong repo, file mẫu có thể đang tên `_env.example` và `_gitignore`. Hãy đổi thành `.env.example` và `.gitignore`.

### Cấu hình `.env`

```env
TELEGRAM_BOT_TOKEN=123456:ABC...
TELEGRAM_CHAT_ID=123456789

# (tuỳ chọn) đăng nhập TradingView để ít bị chặn khi cập nhật giá
# TV_USER=
# TV_PASS=
```

Biến môi trường đặt sẵn trong hệ thống được ưu tiên hơn file `.env`. Không commit file `.env`.

### Dữ liệu và model cần có

| Thành phần | Đường dẫn | Ghi chú |
|---|---|---|
| Dữ liệu thị trường | `data/data_full_market.csv` | Bị `.gitignore` nên **không có sẵn trong repo**, bạn cần tự đặt vào |
| Model xu hướng | `model/trend_model_v3.joblib` | Cần có để chạy dự đoán |
| Kho giá | `data/prices.db` | Tự tạo khi chạy `python DB.py import` |

Mọi đường dẫn nằm trong `paths.py`.

---

## 3. Cách chạy

### Lần đầu

```bash
python DB.py import        # nạp data/data_full_market.csv vào SQLite (làm 1 lần)
python DB.py stats         # kiểm tra DB đang có gì
streamlit run UI.py        # mở giao diện
```

### Hằng ngày

```bash
python DB.py update        # kéo các phiên còn thiếu (nên chạy sau 15:00 ngày giao dịch)
streamlit run UI.py
```

### Quản lý kho giá (`DB.py`)

```bash
python DB.py stats                        # xem DB đang có gì
python DB.py import                       # nạp CSV mặc định vào DB
python DB.py import --csv đường/dẫn.csv   # nạp CSV khác
python DB.py update                       # cập nhật phiên còn thiếu của mọi mã
python DB.py update --liquid              # chỉ mã thanh khoản >= 1 tỷ/phiên (nhanh hơn)
python DB.py update --symbols FPT,ACB     # chỉ định mã (mã mới sẽ tải đủ lịch sử)
```

Mã đã đủ phiên gần nhất sẽ được bỏ qua. `UI.py` chỉ **đọc** từ DB nên có thể chạy `DB.py` riêng, không cần Streamlit hay model.

### Backtest

```bash
python backtest.py         # backtest Euphoria cắt lên 0.8
```

Kết quả lưu trong `backtest_results/`.


---

## 4. Giao diện (4 tab)

| Tab | Chức năng |
|---|---|
| 1. Top xác suất tăng | Bảng xếp hạng toàn thị trường |
| 2. Phân tích 1 mã | Phân tích chi tiết một mã cổ phiếu |
| 3. Lọc SEPA | Danh sách mã thỏa các điều kiện SEPA |
| 4. Cảnh báo thất bại | Mã có dấu hiệu break out thất bại |

---

## 5. Cấu trúc thư mục

Bốn file ở gốc (`UI.py`, `DB.py`, `backtest.py`, `telegram_notify.py`) chỉ là điểm vào mỏng, logic nằm trong các package bên dưới.

```
top_rank_CK/
├── UI.py  DB.py  backtest.py  telegram_notify.py   # điểm vào
├── paths.py                  # đường dẫn dùng chung (DB, model, .env...)
│
├── backend/
│   ├── config.py             # kênh hồi quy, lọc thanh khoản, mã loại trừ (ACM...)
│   ├── preprocess.py         # chuẩn hoá giá thô về dạng train
│   ├── indicators/           # mỗi chỉ báo 1 file
│   │   ├── moving_average.py   sma, ema
│   │   ├── macd.py
│   │   ├── rsi.py              rsi_wilder, rsi_two_bottoms
│   │   ├── adx.py
│   │   ├── regression_channel.py
│   │   └── euphoria.py         chỉ báo hưng phấn [-1, 1] + ngưỡng + trọng số
│   ├── features/             # ghép chỉ báo thành feature cho model
│   │   ├── regime.py           trạng thái D/W/M, nhãn regime
│   │   ├── timeframe.py        gộp nến tuần/tháng
│   │   └── builder.py          build_features (khớp notebook train)
│   ├── prediction/
│   │   ├── model_loader.py     nạp trend_model_v3.joblib
│   │   └── trend.py            predict_trend
│   ├── ranking/
│   │   ├── liquidity.py        Penny filter
│   │   └── scanner.py          quét + xếp hạng toàn thị trường
│   └── screening/
│       ├── sepa/               # bộ lọc SEPA, mỗi điều kiện 1 file
│       │   ├── config.py         ngưỡng (MA, 30%, 25%, số phiên...)
│       │   ├── ma_alignment.py  ma200_rising.py  higher_highs_lows.py
│       │   ├── volume_weeks.py  volume_days.py  off_low.py  near_high.py
│       │   ├── registry.py       danh sách điều kiện
│       │   └── scanner.py
│       └── sepa_failed_breakout/   # cảnh báo break out thất bại
│           ├── config.py  below_ma20.py  lower_lows.py  volume_divergence.py
│           └── registry.py  scanner.py
│
├── database/                 # kho giá SQLite + cập nhật từ TradingView
│   ├── config.py  connection.py  prices.py  universe.py
│   └── sessions.py  tradingview.py  updater.py  live.py  cli.py
│
├── frontend/                 # giao diện Streamlit
│   ├── styles.py             # toàn bộ CSS
│   ├── components.py         # badge, hero header
│   ├── tabs/                 # top_rank.py, stock_detail.py, sepa.py, sepa_exit.py
│   └── sections/             # các khối của tab "Phân tích 1 mã":
│       summary_card, probability, price_chart, euphoria_panel,
│       regime_panel, feature_table, disclaimer
│
├── euphoria_backtest/        # config, data_loader, signals, summary, runner
├── notifier/                 # env, messages, telegram_api, cli
│
├── data/  model/  train/  backtest_results/
└── requirements.txt  .env  .env.example  .gitignore
```

---

## 6. Muốn thêm / sửa thì vào đâu

| Việc | File |
|---|---|
| Thêm chỉ báo mới | tạo `backend/indicators/ten_chi_bao.py`, export trong `indicators/__init__.py` |
| Đổi trọng số / ngưỡng hưng phấn | `backend/indicators/euphoria.py` |
| Đổi bộ lọc thanh khoản, loại mã | `backend/config.py` |
| Đổi ngưỡng SEPA (MA, 30%, 25%...) | `backend/screening/sepa/config.py` |
| Đổi ngưỡng cảnh báo thất bại (MA20, 3 đáy...) | `backend/screening/sepa_failed_breakout/config.py` |
| Thêm điều kiện lọc mới | tạo file trong `backend/screening/sepa/`, thêm 1 dòng vào `registry.py` |
| Đổi cách dự đoán / thêm model | `backend/prediction/` |
| Thêm khối hiển thị ở tab 2 | tạo file trong `frontend/sections/`, gọi trong `frontend/tabs/stock_detail.py` |
| Đổi màu, giao diện | `frontend/styles.py` |
| Đổi ngưỡng / horizon backtest | `euphoria_backtest/config.py` |
| Đổi nguồn / cách cập nhật giá | `database/tradingview.py`, `database/updater.py` |
| Đổi vị trí DB / model / `.env` | `paths.py` |

> ⚠️ `backend/features/builder.py` phải khớp đúng notebook train. Nếu đổi feature thì phải **train lại model**.

---

## 7. Công nghệ sử dụng

- **Giao diện:** Streamlit, Plotly
- **Dữ liệu:** pandas, NumPy, SQLite, `tvdatafeed` (TradingView)
- **Mô hình:** scikit-learn, joblib
- **Thông báo:** Telegram Bot API (requests)

---

## 8. Xử lý sự cố

| Vấn đề | Cách xử lý |
|---|---|
| `python DB.py update` bị chặn hoặc lỗi | Đặt `TV_USER` và `TV_PASS` trong `.env` để đăng nhập TradingView |
| Không có dữ liệu trên giao diện | Chạy `python DB.py import` rồi `python DB.py stats` để kiểm tra |
| Không tìm thấy model | Kiểm tra `model/trend_model_v3.joblib` có tồn tại không |
| Telegram không gửi được | Chạy với `--dry-run` để kiểm tra nội dung, và `--get-chat-id` để kiểm tra lại chat ID |
| Lỗi cài `tvdatafeed` | Cài Git, vì gói này cài trực tiếp từ GitHub |
# AI-Based-Stock-Ranking-System-for-the-Vietnamese-Stock-Market
