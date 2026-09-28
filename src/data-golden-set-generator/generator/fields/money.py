"""Số tiền, số đo theo cách viết Việt Nam: dấu chấm phân cách nghìn, dấu phẩy thập phân, đọc số bằng chữ."""

DIGITS = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
UNITS = ["", " nghìn", " triệu", " tỷ"]


def _read_triple(n: int, full: bool) -> str:
    """Đọc 0-999. full=True khi không phải nhóm đầu, phải đọc cả 'không trăm', 'linh'."""
    tram, chuc, dv = n // 100, n // 10 % 10, n % 10
    words = []
    if full or tram:
        words += [DIGITS[tram], "trăm"]
    if chuc == 0:
        if dv and words:
            words.append("linh")
    elif chuc == 1:
        words.append("mười")
    else:
        words += [DIGITS[chuc], "mươi"]
    if dv:
        if dv == 1 and chuc > 1:
            words.append("mốt")
        elif dv == 5 and chuc > 0:
            words.append("lăm")
        elif dv == 4 and chuc > 1:
            words.append("tư")
        else:
            words.append(DIGITS[dv])
    return " ".join(words)


def to_words(n: int) -> str:
    """1250000 -> 'Một triệu hai trăm năm mươi nghìn'."""
    if n == 0:
        return "Không"
    if n >= 10**12:
        raise ValueError("Chỉ hỗ trợ dưới 1.000 tỷ")
    groups = []
    while n:
        groups.append(n % 1000)
        n //= 1000
    parts = []
    for i in range(len(groups) - 1, -1, -1):
        g = groups[i]
        if g == 0:
            continue
        parts.append(_read_triple(g, full=bool(parts)) + UNITS[i])
    text = " ".join(parts)
    return text[0].upper() + text[1:]


def group(n: int) -> str:
    """1250000 -> '1.250.000'."""
    return f"{n:,}".replace(",", ".")


def decimal(x: float, digits: int = 1) -> str:
    """68.5 -> '68,5'. Bỏ phần thập phân 0."""
    text = f"{x:.{digits}f}".rstrip("0").rstrip(".")
    return text.replace(".", ",")
