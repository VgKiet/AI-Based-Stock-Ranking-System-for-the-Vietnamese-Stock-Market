"""Dựng nội dung tin nhắn (top xác suất tăng / mã thanh khoản lớn) và chia nhỏ theo giới hạn Telegram."""
import html

import backend
import database

from .config import TG_LIMIT


def build_rank_message(top: int, min_value: float) -> str:
    symbols, _ = backend.load_universe(0, min_value)
    if not symbols:
        raise SystemExit("Không có mã nào thoả điều kiện thanh khoản (DB trống?).")
    df, failed = backend.scan_universe(symbols)
    if df.empty:
        raise SystemExit("Model không cho ra kết quả. Kiểm tra DB và model.")
    df = df.head(top)

    lines = [f"{'#':>2} {'Mã':<5}{'Sàn':<6}{'Giá':>7} {'P(tăng)':>7}  Dự báo"]
    for i, r in df.iterrows():
        lines.append(f"{i + 1:>2} {r['Mã']:<5}{str(r['Sàn']):<6}{r['Giá']:>7.2f} {r['P(tăng)']:>7.1%}  {r['Dự báo']}")
    head = (f"🏆 <b>Top {len(df)} mã xác suất tăng cao nhất</b>\n"
            f"Thanh khoản ≥ {min_value:g} tỷ/phiên · quét {len(symbols)} mã · dữ liệu tới {df['Ngày'].max()}\n")
    foot = "\n⚠️ Chỉ mang tính tham khảo, không phải khuyến nghị mua/bán."
    return head + "<pre>" + html.escape("\n".join(lines)) + "</pre>" + foot


def build_liquid_message(top: int, min_value: float) -> str:
    symbols, ex = database.db_universe(top, min_value)
    if not symbols:
        raise SystemExit("Không có mã nào thoả điều kiện thanh khoản (DB trống?).")
    rows = [f"{s}({ex.get(s, '?')})" for s in symbols]
    body = "\n".join(", ".join(rows[i:i + 5]) for i in range(0, len(rows), 5))
    return (f"💧 <b>{len(symbols)} mã thanh khoản lớn nhất</b> (≥ {min_value:g} tỷ/phiên)\n"
            f"<pre>{html.escape(body)}</pre>")


def split_message(text: str, limit: int = TG_LIMIT):
    """Chia tin dài theo dòng; mỗi phần giữ nguyên thẻ <pre> để vẫn hiển thị đúng."""
    if len(text) <= limit:
        return [text]
    head, rest = text.split("<pre>", 1)
    table, foot = rest.split("</pre>", 1)
    parts, cur = [], []
    size = 0
    for ln in table.split("\n"):
        if size + len(ln) + 1 > limit - 200:
            parts.append(cur); cur, size = [], 0
        cur.append(ln); size += len(ln) + 1
    parts.append(cur)
    out = []
    for i, p in enumerate(parts):
        out.append((head if i == 0 else "") + "<pre>" + "\n".join(p) + "</pre>" + (foot if i == len(parts) - 1 else ""))
    return out
