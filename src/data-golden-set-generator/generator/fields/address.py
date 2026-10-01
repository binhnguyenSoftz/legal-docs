"""Địa chỉ theo hai thời kỳ.

- Trước 01/7/2025: 3 cấp (tỉnh - huyện - xã), dùng cho giấy tờ cũ.
- Từ 01/7/2025: 2 cấp (tỉnh - xã).

Mỗi địa chỉ sinh ra mang cả hai cách ghi của cùng một nơi (units_pre2025.csv ánh xạ xã cũ -> xã mới, toàn quốc),
để sinh ca "cùng một nơi, hai cách ghi" cho AIP-008. Giấy tờ chọn cách ghi theo ngày lập (`at`).
Phần chi tiết (số nhà, ngõ, hẻm, thôn, ấp...) theo kiểu từng vùng và thành thị/nông thôn.
"""

import csv
import random
from datetime import date
from functools import cache

from generator import RESOURCES_DIR

REFORM_DATE = date(2025, 7, 1)
URBAN_RATE = 0.5  # Danh mục đa số là xã; nâng tỷ lệ phường, thị trấn cho gần với hồ sơ nhà đất

STREETS = [
    "Lê Lợi", "Trần Hưng Đạo", "Nguyễn Trãi", "Hai Bà Trưng", "Lý Thường Kiệt", "Quang Trung", "Hùng Vương",
    "Phan Chu Trinh", "Lê Duẩn", "Nguyễn Huệ", "Trần Phú", "Lê Hồng Phong", "Nguyễn Du", "Phan Đình Phùng",
    "Điện Biên Phủ", "Nguyễn Văn Cừ", "Lý Thái Tổ", "Trần Quang Khải", "Ngô Quyền", "Bà Triệu", "Lê Thánh Tông",
    "Nguyễn Thị Minh Khai", "Võ Thị Sáu", "Cách Mạng Tháng Tám", "Nguyễn Đình Chiểu", "Pasteur", "Hoàng Văn Thụ",
    "Phạm Văn Đồng", "Tôn Đức Thắng", "Nguyễn Tri Phương", "Lê Văn Sỹ", "Nguyễn Chí Thanh", "Trường Chinh",
    "Lạc Long Quân", "Âu Cơ", "Chu Văn An", "Tô Hiến Thành", "Lê Quý Đôn", "Nguyễn Khuyến", "Phan Bội Châu",
    "Huỳnh Thúc Kháng", "Nguyễn Thái Học", "Đinh Tiên Hoàng", "Lê Đại Hành", "Mạc Đĩnh Chi", "Yết Kiêu",
    "Hoàng Diệu", "Nguyễn Công Trứ", "Bạch Đằng", "Hàm Nghi", "Duy Tân", "Thống Nhất", "Độc Lập", "Hòa Bình",
    "Nguyễn Văn Linh", "Võ Văn Kiệt", "30 Tháng 4", "3 Tháng 2", "Kha Vạn Cân", "Lũy Bán Bích",
]
HAMLETS = [
    "Đông", "Tây", "Nam", "Bắc", "Trung", "Thượng", "Hạ", "Mới", "Tân Lập", "Tân Thành", "An Hòa", "Phú Lợi",
    "Hòa Bình", "Thành Công", "Quyết Tiến", "Đoàn Kết", "Thắng Lợi", "Bình An", "Long Hòa", "Mỹ Phước",
    "Phú Thọ", "Tân Phú", "Hưng Long", "Vĩnh Hòa", "Cầu Đá", "Bến Đò", "Gò Cao", "Đồng Tâm", "Tiền Phong", "Hợp Nhất",
]
# Mã thống kê tỉnh cũ: vùng núi phía Bắc dùng "bản", Tây Nguyên có "buôn".
MOUNTAIN = {"02", "04", "06", "08", "10", "11", "12", "14", "15", "17", "20"}
HIGHLAND = {"62", "64", "66", "67", "68"}


@cache
def units() -> list[dict]:
    with open(RESOURCES_DIR / "admin" / "units_pre2025.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


@cache
def _split() -> tuple[list[dict], list[dict]]:
    urban = [u for u in units() if not u["ward"].startswith("Xã")]
    rural = [u for u in units() if u["ward"].startswith("Xã")]
    return urban, rural


@cache
def _province_code() -> dict[str, str]:
    with open(RESOURCES_DIR / "admin" / "cccd_province_codes.csv", encoding="utf-8") as f:
        return {r["province"]: r["code"][1:] for r in csv.DictReader(f)}


def region(province: str) -> str:
    """north | central | south theo mã thống kê tỉnh cũ."""
    code = int(_province_code().get(province, "01"))
    return "north" if code < 38 else "central" if code < 70 else "south"


def _detail(rng: random.Random, unit: dict) -> tuple[str, str | None]:
    """(chi tiết, tên đường nếu có)."""
    n, m, k = rng.randint(1, 350), rng.randint(2, 180), rng.randint(1, 40)
    street = rng.choice(STREETS)
    code = _province_code().get(unit["province"], "01")
    reg = region(unit["province"])
    if unit["ward"].startswith("Xã"):
        if code in MOUNTAIN and rng.random() < 0.6:
            kind = "Bản"
        elif code in HIGHLAND and rng.random() < 0.3:
            kind = "Buôn"
        else:
            kind = {"north": rng.choice(["Thôn", "Xóm"]), "central": "Thôn", "south": "Ấp"}[reg]
        name = str(rng.randint(1, 12)) if rng.random() < 0.4 else rng.choice(HAMLETS)
        return f"{kind} {name}", None
    if unit["ward"].startswith("Thị trấn") and rng.random() < 0.5:
        return rng.choice([f"Khu phố {rng.randint(1, 12)}", f"Tổ dân phố {rng.randint(1, 20)}"]), None
    if code == "01":
        return rng.choice([f"Số {n} phố {street}", f"Số {n} ngõ {m} phố {street}",
                           f"Số {k}, ngách {m}/{rng.randint(1, 30)}, ngõ {m} {street}"]), street
    if reg == "south":
        return rng.choice([f"Số {n} đường {street}", f"{n}/{m} {street}", f"{n}/{m}/{k} {street}",
                           f"Tổ {k}, khu phố {rng.randint(1, 9)}"]), street
    if reg == "central":
        return rng.choice([f"Số {n} đường {street}", f"K{n}/{k} {street}", f"Tổ {k}"]), street
    return rng.choice([f"Số {n} đường {street}", f"Số nhà {n}, ngõ {m} đường {street}",
                       f"Tổ dân phố {rng.randint(1, 30)}"]), street


def generate(rng: random.Random, province: str | None = None) -> dict:
    """province: chỉ lấy địa chỉ thuộc tỉnh/thành phố này (tên sau 01/7/2025), ví dụ 'Thành phố Hồ Chí Minh'."""
    urban, rural = _split()
    if province:
        urban = [u for u in urban if u["new_province"] == province]
        rural = [u for u in rural if u["new_province"] == province]
        if not urban and not rural:
            raise ValueError(f"Không có đơn vị hành chính nào thuộc {province}")
    want_urban = rng.random() < URBAN_RATE
    unit = rng.choice(urban if want_urban and urban or not rural else rural)
    detail, street = _detail(rng, unit)
    return {
        "chi_tiet": detail,
        "duong": street if street and street in detail else None,
        "xa": unit["new_commune"],
        "tinh": unit["new_province"],
        "xa_cu": unit["ward"],
        "huyen_cu": unit["district"],
        "tinh_cu": unit["province"],
        "tinh_cu_ngan": short_province(unit["province"]),
    }


def short_province(name: str) -> str:
    """'Thành phố Hồ Chí Minh' -> 'Hồ Chí Minh', 'Tỉnh Quảng Nam' -> 'Quảng Nam' (cách viết trong giấy viết tay)."""
    for prefix in ("Thành phố ", "Tỉnh "):
        if name.startswith(prefix):
            return name[len(prefix):]
    return name


def format(addr: dict) -> str:
    return ", ".join([addr["chi_tiet"], addr["xa"], addr["tinh"]])


def format_old(addr: dict) -> str:
    return ", ".join([addr["chi_tiet"], addr["xa_cu"], addr["huyen_cu"], addr["tinh_cu"]])


def format_at(addr: dict, at: date) -> str:
    """Cách ghi đúng với giấy tờ lập ngày `at`."""
    return format(addr) if at >= REFORM_DATE else format_old(addr)


def place(addr: dict, at: date) -> str:
    """Chỉ đơn vị hành chính, không có số nhà: dùng cho quê quán, nơi sinh."""
    if at >= REFORM_DATE:
        return f"{addr['xa']}, {addr['tinh']}"
    return f"{addr['xa_cu']}, {addr['huyen_cu']}, {addr['tinh_cu']}"
