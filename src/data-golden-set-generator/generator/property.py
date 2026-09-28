"""Thửa đất và nhà trên đất, dùng chung cho giấy chứng nhận, bản vẽ hiện trạng, tờ đăng ký, giấy sang đất.

Thửa đất là tứ giác gần chữ nhật: mặt tiền rộng `rong_truoc`, mặt hậu `rong_sau`, chiều sâu hai cạnh bên.
Tọa độ tính bằng mét, gốc ở góc trái mặt tiền, trục y hướng vào trong thửa.
"""

import math
import random
from datetime import date

from generator.fields import money, names

STRUCTURES = [
    "Tường gạch, mái tôn",
    "Tường gạch, mái ngói",
    "Khung BTCT, tường gạch, sàn BTCT, mái tôn",
    "Khung BTCT, tường gạch, sàn BTCT, mái BTCT",
]
LAND_USE = ["Sử dụng riêng", "Sử dụng riêng", "Sử dụng chung"]
DIRECTIONS = ["Đông", "Tây", "Nam", "Bắc"]
OPPOSITE = {"Đông": "Tây", "Tây": "Đông", "Nam": "Bắc", "Bắc": "Nam"}
# Bản vẽ đặt mặt tiền ở dưới. Hướng mặt tiền -> (hướng cạnh bên phải bản vẽ, góc mũi tên chỉ Bắc so với chiều lên).
RIGHT_OF = {"Nam": ("Đông", 0), "Bắc": ("Tây", 180), "Đông": ("Bắc", 90), "Tây": ("Nam", -90)}


def _area(poly: list[tuple[float, float]]) -> float:
    s = 0.0
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        s += x0 * y1 - x1 * y0
    return abs(s) / 2


def _edge(a, b) -> float:
    return math.dist(a, b)


def _neighbor(rng: random.Random) -> str:
    gender = rng.choice(["male", "female"])
    n = names.generate(rng, gender)
    return f"Nhà {'ông' if gender == 'male' else 'bà'} {n['ho_ten']}"


def _price(rng: random.Random, bought: date) -> dict:
    """Giá sang nhượng: trước 1993 hay ghi bằng vàng, sau đó chủ yếu bằng tiền đồng."""
    if bought.year < 1993 and rng.random() < 0.7:
        luong = rng.randint(2, 25)
        return {"don_vi": "vang", "so": luong, "text": f"{luong} lượng vàng 24K",
                "bang_chu": f"{money.to_words(luong)} lượng vàng 24K"}
    trieu = rng.randint(10, 400) if bought.year >= 1993 else rng.randint(2, 40)
    amount = trieu * 1_000_000 + rng.choice([0, 0, 500_000])
    return {"don_vi": "dong", "so": amount, "text": f"{money.group(amount)} đồng",
            "bang_chu": f"{money.to_words(amount)} đồng"}


def build(rng: random.Random, addr: dict, bought: date, built_before: date) -> dict:
    front = round(rng.uniform(3.5, 8.0), 2)
    back = round(front + rng.choice([0, 0, rng.uniform(-0.6, 0.6)]), 2)
    depth_l = round(rng.uniform(8.0, 25.0), 2)
    depth_r = round(depth_l + rng.choice([0, rng.uniform(-0.8, 0.8)]), 2)
    offset = rng.uniform(-0.3, 0.3)
    poly = [(0.0, 0.0), (front, 0.0), (offset + back, depth_r), (offset, depth_l)]
    dien_tich = round(_area(poly), 1)

    ratio = rng.uniform(0.7, 1.0)
    so_tang = rng.choice([1, 1, 2, 2, 3, 4])
    xd = round(dien_tich * ratio, 1)
    street = addr.get("duong") or "hẻm chung"
    facing = rng.choice(DIRECTIONS)
    right, north_angle = RIGHT_OF[facing]
    # Thứ tự cạnh như polygon: mặt tiền, phải, mặt hậu, trái.
    edge_dirs = [facing, right, OPPOSITE[facing], OPPOSITE[right]]
    tu_can = {facing: f"Đường {street}" if street != "hẻm chung" else "Hẻm chung"}
    for d in edge_dirs[1:]:
        tu_can[d] = _neighbor(rng)

    return {
        "dia_chi_parts": addr,
        "so_thua": str(rng.randint(1, 999)),
        "to_ban_do": str(rng.randint(1, 80)),
        "polygon": [(round(x, 2), round(y, 2)) for x, y in poly],
        "canh": [round(_edge(a, b), 2) for a, b in zip(poly, poly[1:] + poly[:1])],
        "dien_tich": dien_tich,
        "hinh_thuc_su_dung": rng.choice(LAND_USE),
        "muc_dich": "Đất ở",
        "nha": {
            "so_tang": so_tang,
            "ket_cau": STRUCTURES[min(len(STRUCTURES) - 1, so_tang - 1 + rng.randint(0, 1))],
            "dien_tich_xay_dung": xd,
            "dien_tich_san": round(xd * so_tang, 1),
            "nam_xay_dung": rng.randint(bought.year, max(bought.year, min(bought.year + 5, built_before.year))),
            "ty_le": ratio,
        },
        "huong": facing,
        "huong_canh": edge_dirs,
        "goc_bac": north_angle,
        "tu_can": tu_can,
        "tu_can_canh": [tu_can[d] for d in edge_dirs],
        "gia_sang": _price(rng, bought),
    }
