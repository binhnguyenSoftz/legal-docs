"""Số định danh cá nhân (12 số, in trên CCCD/thẻ căn cước).

Cấu trúc: 3 số mã nơi đăng ký khai sinh + 1 số mã thế kỷ và giới tính
+ 2 số cuối năm sinh + 6 số ngẫu nhiên.
Mã thế kỷ/giới tính: thế kỷ 20 nam 0 nữ 1, thế kỷ 21 nam 2 nữ 3, thế kỷ 22 nam 4 nữ 5...
"""

import csv
import random
from datetime import date, timedelta
from functools import cache

from generator import RESOURCES_DIR
from generator.fields.dates import add_years

# Tuổi phải đổi thẻ theo Luật Căn cước 2023. Sau 60 tuổi thẻ không ghi thời hạn.
RENEW_AGES = (14, 25, 40, 60)
# CCCD mã vạch cấp từ 2016, nên thẻ còn hạn sớm nhất có thể cấp từ đây.
EARLIEST_ISSUE = date(2016, 1, 1)

# Thế hệ thẻ theo ngày cấp: (loại, cấp từ ngày, nơi cấp in trên thẻ).
# [CẦN XÁC NHẬN] mốc chuyển chính xác giữa các thế hệ và chức danh nơi cấp.
GENERATIONS = [
    ("cccd-ma-vach", date(2016, 1, 1), "Cục trưởng Cục Cảnh sát ĐKQL cư trú và DLQG về dân cư"),
    ("cccd-chip", date(2021, 1, 15), "Cục trưởng Cục Cảnh sát quản lý hành chính về trật tự xã hội"),
    ("the-can-cuoc", date(2024, 7, 1), "Bộ Công an"),
]
CMND = "cmnd-9"
# CMND hết giá trị từ 01/01/2025 (Luật Căn cước 2023, Điều 46).
CMND_VALID_UNTIL = date(2024, 12, 31)
CMND_YEARS = 15

IDENTIFYING_MARKS = [
    "Nốt ruồi C:1cm trên sau đầu mày trái", "Nốt ruồi C:2cm dưới sau mép phải",
    "Sẹo chấm C:1,5cm trên trước đầu mày phải", "Nốt ruồi C:3cm dưới trước cánh mũi trái",
    "Sẹo chấm C:2cm dưới sau đuôi mắt trái", "Nốt ruồi C:1cm trên sau cánh mũi phải",
]


@cache
def _provinces() -> list[dict]:
    with open(RESOURCES_DIR / "admin" / "cccd_province_codes.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def province_codes() -> list[str]:
    return [row["code"] for row in _provinces()]


def code_for(province: str) -> str | None:
    return next((r["code"] for r in _provinces() if r["province"] == province), None)


def cmnd_prefix_for(province: str) -> str:
    """Đầu số CMND 9 số theo tỉnh cấp. Chưa có trong bảng thì tạm dùng mã thống kê 2 số của tỉnh.

    [CẦN XÁC NHẬN] cột cmnd_prefix mới có 5 tỉnh; bảng đầy đủ theo NĐ 05/1999/NĐ-CP.
    """
    row = next((r for r in _provinces() if r["province"] == province), _provinces()[0])
    return row["cmnd_prefix"] or row["code"][1:]


def century_gender_digit(dob: date, gender: str) -> int:
    century_index = dob.year // 100 - 19  # 1900s -> 0, 2000s -> 1
    return century_index * 2 + (1 if gender == "female" else 0)


def generate(rng: random.Random, dob: date, gender: str, province_code: str | None = None) -> str:
    code = province_code or rng.choice(province_codes())
    return f"{code}{century_gender_digit(dob, gender)}{dob.year % 100:02d}{rng.randrange(10**6):06d}"


def validate(number: str, dob: date, gender: str) -> list[str]:
    """Trả về danh sách lỗi, rỗng nếu khớp ngày sinh và giới tính."""
    errors = []
    if len(number) != 12 or not number.isdigit():
        return ["Không đủ 12 chữ số"]
    if int(number[3]) != century_gender_digit(dob, gender):
        errors.append("Mã thế kỷ/giới tính không khớp")
    if number[4:6] != f"{dob.year % 100:02d}":
        errors.append("Năm sinh không khớp")
    return errors


def expiry_date(dob: date, issue_date: date) -> date | None:
    """Ngày hết hạn in trên thẻ. None nghĩa là không thời hạn.

    Thẻ cấp trong vòng 2 năm trước mốc đổi thẻ thì có giá trị tới mốc kế tiếp.
    """
    for i, age in enumerate(RENEW_AGES):
        milestone = add_years(dob, age)
        if issue_date >= milestone:
            continue
        if issue_date >= add_years(milestone, -2):
            if i + 1 < len(RENEW_AGES):
                return add_years(dob, RENEW_AGES[i + 1])
            return None
        return milestone
    return None


def issue_date(rng: random.Random, dob: date, as_of: date, window: tuple[date, date] | None = None) -> date | None:
    """Ngày cấp sao cho thẻ còn hạn tại as_of. None nếu chưa đủ 14 tuổi.

    window: chỉ cấp trong khoảng này (để ép thế hệ thẻ). None nếu không có ngày cấp nào vừa trong khoảng vừa còn hạn.
    """
    lower = max(EARLIEST_ISSUE, add_years(dob, 14))
    upper = as_of.fromordinal(as_of.toordinal() - 1)
    if lower > upper:
        return None
    # Thẻ phải cấp sau (mốc đổi thẻ gần nhất đã qua - 2 năm), nếu không đã hết hạn.
    passed = [add_years(dob, a) for a in RENEW_AGES if add_years(dob, a) <= as_of]
    if passed:
        lower = max(lower, add_years(passed[-1], -2))
    if window:
        lower, upper = max(lower, window[0]), min(upper, window[1])
        if lower > upper:
            return None
    lower = min(lower, upper)
    return date.fromordinal(rng.randint(lower.toordinal(), upper.toordinal()))


def generation_window(kind: str) -> tuple[date, date]:
    """Khoảng ngày cấp của một thế hệ thẻ."""
    names = [g[0] for g in GENERATIONS]
    i = names.index(kind)
    end = GENERATIONS[i + 1][1] - timedelta(days=1) if i + 1 < len(GENERATIONS) else date.max
    return GENERATIONS[i][1], end


def generation(issued: date) -> tuple[str, str]:
    """(loại thẻ, nơi cấp) theo ngày cấp."""
    kind, place = GENERATIONS[0][0], GENERATIONS[0][2]
    for k, start, p in GENERATIONS:
        if issued >= start:
            kind, place = k, p
    return kind, place


def cmnd_generate(rng: random.Random, province: str) -> str:
    prefix = cmnd_prefix_for(province)
    return prefix + "".join(str(rng.randrange(10)) for _ in range(9 - len(prefix)))


def cmnd_issue_date(rng: random.Random, dob: date, until: date) -> date | None:
    """Ngày cấp CMND: từ 14 tuổi, trong khoảng 1980-2015. None nếu không có khoảng hợp lệ."""
    lower = max(add_years(dob, 14), date(1980, 1, 1))
    upper = min(date(2015, 12, 31), until)
    if lower > upper:
        return None
    return date.fromordinal(rng.randint(lower.toordinal(), upper.toordinal()))


def _mrz_check(s: str) -> str:
    """Chữ số kiểm tra ICAO 9303: trọng số 7-3-1."""
    def val(c):
        if c.isdigit():
            return int(c)
        if c == "<":
            return 0
        return ord(c) - 55
    return str(sum(val(c) * (7, 3, 1)[i % 3] for i, c in enumerate(s)) % 10)


def mrz(number: str, dob: date, gender: str, expiry: date | None, ho_ten_ascii: str) -> list[str]:
    """MRZ 3 dòng (TD1, 30 ký tự) in ở mặt sau CCCD gắn chip và thẻ căn cước.

    [CẦN XÁC NHẬN] bố cục trường tùy chọn ở dòng 1 so với thẻ thật.
    """
    doc_no = number[-9:]
    line1 = f"IDVNM{doc_no}{_mrz_check(doc_no)}{number}".ljust(30, "<")[:30]
    b = dob.strftime("%y%m%d")
    e = expiry.strftime("%y%m%d") if expiry else "<<<<<<"
    body = f"{b}{_mrz_check(b)}{'F' if gender == 'female' else 'M'}{e}{_mrz_check(e)}VNM"
    line2 = body.ljust(29, "<")
    composite = line1[5:30] + line2[0:7] + line2[8:15] + line2[18:29]
    line2 += _mrz_check(composite)
    parts = ho_ten_ascii.upper().split()
    line3 = (parts[0] + "<<" + "<".join(parts[1:])).ljust(30, "<")[:30]
    return [line1, line2, line3]
