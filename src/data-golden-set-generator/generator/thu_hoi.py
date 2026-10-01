"""Đợt thu hồi đất và số liệu bồi thường của một hồ sơ, theo quy định TP.HCM (bộ quy định `tphcm-2026`).

Dùng chung cho 5 giấy tờ đầu ra của thủ tục giai-toa-den-bu-tphcm: GXN 1131, bảng chiết tính bồi thường đất,
bảng chiết tính bồi thường công trình, quyết định khen thưởng, quyết định tái định cư.
Công thức và giả định: specs/de-xuat-giay-to-boi-thuong.md. Mọi số tiền là số nguyên đồng.

Dòng thời gian (sau ngày nộp hồ sơ):
  nộp hồ sơ -> GXN (ngay_gxn) -> quyết định thu hồi và phê duyệt phương án (ngay_qd)
  -> quyết định tái định cư (ngay_qd_tdc) -> bàn giao mặt bằng (ngay_ban_giao, hạn han_ban_giao)
  -> quyết định khen thưởng (ngay_qd_thuong).
"""

import random
from datetime import date, timedelta

from generator.fields import dates

# Quyết định 11/2026/QĐ-UBND TP.HCM có hiệu lực từ 06/3/2026: giấy tờ đầu ra lập từ mốc này.
EFFECTIVE = date(2026, 3, 6)

# Diện tích tối thiểu còn lại để ở được. [CẦN XÁC NHẬN] theo quy định diện tích tối thiểu tách thửa của TP.HCM.
MIN_RESIDUAL = 36.0

# Đơn giá xây mới (đ/m² sàn) và niên hạn sử dụng (năm) theo kết cấu. [GIẢ LẬP] chưa lấy từ bảng đơn giá thật.
BUILD_PRICE = {
    "Tường gạch, mái tôn": (3_200_000, 30),
    "Tường gạch, mái ngói": (3_600_000, 40),
    "Khung BTCT, tường gạch, sàn BTCT, mái tôn": (6_300_000, 60),
    "Khung BTCT, tường gạch, sàn BTCT, mái BTCT": (7_200_000, 80),
}
MIN_REMAINING_RATE = 20     # Tỷ lệ chất lượng còn lại thấp nhất (%)
FLOOR_RATE = 60             # QĐ 11/2026: giá trị hiện có dưới 60% giá xây mới thì bồi thường bổ sung lên 60%
YARD_PRICE = 165_000        # Sân láng xi măng, đ/m² [GIẢ LẬP]
FENCE_PRICE = 720_000       # Tường rào gạch, đ/m dài [GIẢ LẬP]
WELL_PRICE = 3_500_000      # Giếng khoan, đ/cái [GIẢ LẬP]

# Thưởng bàn giao mặt bằng đúng hạn (QĐ 11/2026): hộ gia đình, cá nhân.
REWARD_FULL_CAP = 50_000_000
REWARD_PART_CAP = 25_000_000

# Suất tái định cư tối thiểu (m²) [CẦN XÁC NHẬN]. Hỗ trợ tự lo chỗ ở: % tiền bồi thường đất [CẦN XÁC NHẬN].
MIN_APARTMENT = 36.0
MIN_LOT = 50.0
SELF_ARRANGE_RATE = 0.05

TDC_FORMS = ["can-ho", "nen-dat", "tu-lo-cho-o", "khong"]
TDC_TITLES = {"can-ho": "Căn hộ chung cư", "nen-dat": "Nền đất tái định cư", "tu-lo-cho-o": "Tự lo chỗ ở"}

PROJECTS = [
    "Dự án mở rộng đường {duong}",
    "Dự án nâng cấp, mở rộng hẻm và hệ thống thoát nước {xa}",
    "Dự án xây dựng Trường Tiểu học {xa}",
    "Dự án xây dựng công viên cây xanh {xa}",
    "Dự án cải tạo, chỉnh trang rạch {xa}",
]


def _round(x: float, unit: int = 1) -> int:
    return int(round(x / unit)) * unit


def _remaining_rate(ket_cau: str, age: int) -> int:
    _, life = BUILD_PRICE[ket_cau]
    return max(MIN_REMAINING_RATE, round(100 - 100 * age / life))


def _building_rows(prop: dict, ratio: float, full_demolition: bool, at: date, rng: random.Random) -> list[dict]:
    """Các dòng bảng chiết tính công trình. ratio: phần diện tích đất bị thu hồi (0-1]."""
    nha = prop["nha"]
    price, _ = BUILD_PRICE[nha["ket_cau"]]
    k = 1.0 if full_demolition else ratio
    rate = _remaining_rate(nha["ket_cau"], at.year - nha["nam_xay_dung"])
    kl = round(nha["dien_tich_san"] * k, 1)
    new_value = _round(kl * price)
    current = _round(new_value * rate / 100)
    extra = max(0, _round(new_value * FLOOR_RATE / 100) - current)
    rows = [{"hang_muc": "Nhà ở chính", "ket_cau": nha["ket_cau"], "don_vi": "m² sàn", "khoi_luong": kl,
             "don_gia": price, "ty_le": rate, "gia_tri_hien_co": current, "bo_sung": extra,
             "thanh_tien": current + extra}]

    def vkt(name, structure, unit, qty, unit_price):
        qty = round(qty, 1)
        amount = _round(qty * unit_price)
        rows.append({"hang_muc": name, "ket_cau": structure, "don_vi": unit, "khoi_luong": qty, "don_gia": unit_price,
                     "ty_le": 100, "gia_tri_hien_co": amount, "bo_sung": 0, "thanh_tien": amount})

    yard = prop["dien_tich"] - nha["dien_tich_xay_dung"]
    if yard >= 1:
        vkt("Sân", "Láng xi măng", "m²", yard * k, YARD_PRICE)
    if full_demolition and rng.random() < 0.5:
        vkt("Tường rào", "Xây gạch, cao 1,8 m", "m", sum(prop["canh"][1:]), FENCE_PRICE)
    if rng.random() < 0.3:
        vkt("Giếng khoan", "Ống nhựa, sâu 30 m", "cái", 1, WELL_PRICE)
    return rows


def _tdc(rng: random.Random, form: str, land_money: int, xa: str) -> dict:
    """Suất tái định cư. Tiền bồi thường đất trừ vào giá suất; thiếu so với suất tối thiểu thì Nhà nước hỗ trợ."""
    ten_xa = xa.split(" ", 1)[1]
    out = {"hinh_thuc": form, "ten": TDC_TITLES.get(form, "Không đủ điều kiện"), "du_dieu_kien": form != "khong",
           "so_suat": 1 if form != "khong" else 0}
    if form == "khong":
        return out
    apt_price = rng.randint(18_000, 30_000) * 1000
    if form == "nen-dat":
        unit_price = rng.randint(10_000, 45_000) * 1000
        area = round(rng.uniform(MIN_LOT, 100), 1)
        min_value = _round(MIN_LOT * unit_price)
        letter = rng.choice("ABCDEFGH")
        out |= {"khu": f"Khu tái định cư {ten_xa}", "lo": f"Lô {letter}{rng.randint(1, 12)}",
                "so_nen": str(rng.randint(1, 60))}
    else:
        unit_price = apt_price
        area = round(rng.uniform(45, 75), 1)
        min_value = _round(MIN_APARTMENT * apt_price)
        block = rng.choice("ABCDE")
        floor = rng.randint(2, 15)
        out |= {"khu": f"Chung cư tái định cư {ten_xa}", "block": f"Lô {block}", "tang": floor,
                "so_can": f"{block}.{floor:02d}.{rng.randint(1, 16):02d}"}
    support = max(0, min_value - land_money)
    out |= {"gia_suat_toi_thieu": min_value, "ho_tro_suat_toi_thieu": support}
    if form == "tu-lo-cho-o":
        out["ho_tro_tu_lo"] = _round(land_money * SELF_ARRANGE_RATE, 1000)
        for k in ("khu", "block", "tang", "so_can"):
            out.pop(k)
        return out
    price = _round(area * unit_price, 1000)
    diff = price - land_money - support
    return out | {"dien_tich": area, "don_gia": unit_price, "gia": price,
                  "tien_phai_nop": max(0, diff), "tien_duoc_nhan": max(0, -diff)}


def build(rng: random.Random, dossier: dict, knobs: dict, override: dict | None = None) -> dict:
    """knobs: thu_hoi.pham_vi (toan-bo | mot-phan), thu_hoi.ban_giao (dung-han | tre-han), thu_hoi.tdc (TDC_FORMS).
    Không có knob thì chọn ngẫu nhiên. override: ca lỗi M17 (khen_thuong_khi_tre)."""
    override = override or {}
    prop, submit = dossier["property"], dossier["submit_date"]
    addr = prop["dia_chi_parts"]
    pham_vi = knobs.get("thu_hoi.pham_vi") or rng.choice(["toan-bo", "toan-bo", "mot-phan"])
    ban_giao = knobs.get("thu_hoi.ban_giao") or rng.choice(["dung-han", "dung-han", "dung-han", "tre-han"])
    tdc = knobs.get("thu_hoi.tdc") or rng.choice(TDC_FORMS)
    want_tdc = tdc != "khong"

    # Diện tích thu hồi. Thu hồi một phần: phần còn lại dưới MIN_RESIDUAL thì không đủ để ở, nhà phải phá cả căn.
    area = prop["dien_tich"]
    co_cho_o_khac = False
    if pham_vi == "toan-bo":
        residual = 0.0
        co_cho_o_khac = not want_tdc
    elif want_tdc or area * 0.8 < MIN_RESIDUAL:
        residual = round(rng.uniform(max(5.0, area * 0.1), min(MIN_RESIDUAL - 0.1, area * 0.8)), 1)
        co_cho_o_khac = not want_tdc
    else:
        residual = round(rng.uniform(MIN_RESIDUAL, area * 0.8), 1)
    thu_hoi_dt = round(area - residual, 1)
    residual = round(area - thu_hoi_dt, 1)
    khong_du_o = residual < MIN_RESIDUAL

    urban = addr["xa"].startswith("Phường")
    gia_dat = rng.randint(30_000, 250_000) * 1000 if urban else rng.randint(5_000, 40_000) * 1000

    ngay_gxn = submit + timedelta(days=rng.randint(5, 20))
    ngay_qd = max(EFFECTIVE, ngay_gxn + timedelta(days=rng.randint(10, 40)))
    han = ngay_qd + timedelta(days=rng.randint(45, 90))
    if ban_giao == "dung-han":
        ngay_ban_giao = dates.between(rng, max(ngay_qd + timedelta(days=15), han - timedelta(days=30)), han)
    else:
        ngay_ban_giao = han + timedelta(days=rng.randint(5, 60))
    khen_thuong = ban_giao == "dung-han" or bool(override.get("khen_thuong_khi_tre"))

    land_rows = [{"noi_dung": "Đất ở (có giấy chứng nhận)", "dien_tich": thu_hoi_dt, "don_gia": gia_dat, "ty_le": 100,
                  "thanh_tien": _round(thu_hoi_dt * gia_dat)}]
    tien_dat = sum(r["thanh_tien"] for r in land_rows)
    building = _building_rows(prop, thu_hoi_dt / area, khong_du_o, ngay_qd, rng)
    tien_ct = sum(r["thanh_tien"] for r in building)
    if pham_vi == "toan-bo":
        thuong = min(tien_dat, REWARD_FULL_CAP)
    else:
        thuong = min(_round(tien_dat * 0.5), REWARD_PART_CAP)

    duong = addr.get("duong") or rng.choice(["Liên Phường", "Tỉnh lộ 10", "Hương lộ 2", "Nguyễn Văn Tạo"])
    project = rng.choice(PROJECTS).format(duong=duong, xa=addr["xa"].split(" ", 1)[1])
    return {
        "co_quan": addr["xa"],
        "ten_du_an": project,
        "so_qd": f"{rng.randint(100, 2999)}/QĐ-UBND",
        "ngay_qd": ngay_qd,
        "so_gxn": f"{rng.randint(10, 999)}/GXN-UBND",
        "ngay_gxn": ngay_gxn,
        "pham_vi": pham_vi,
        "pham_vi_text": "Thu hồi toàn bộ thửa đất" if pham_vi == "toan-bo" else "Thu hồi một phần thửa đất",
        "dien_tich": thu_hoi_dt,
        "dien_tich_con_lai": residual,
        "khong_du_o": khong_du_o,
        "co_cho_o_khac": co_cho_o_khac,
        "gia_dat": gia_dat,
        "dat": land_rows,
        "tien_bt_dat": tien_dat,
        "cong_trinh": building,
        "tien_bt_cong_trinh": tien_ct,
        "han_ban_giao": han,
        "ngay_ban_giao": ngay_ban_giao,
        "ban_giao": ban_giao,
        "co_khen_thuong": khen_thuong,
        "tien_thuong": thuong if khen_thuong else 0,
        "so_qd_thuong": f"{rng.randint(100, 2999)}/QĐ-UBND",
        "ngay_qd_thuong": ngay_ban_giao + timedelta(days=rng.randint(7, 30)),
        "tdc": _tdc(rng, tdc, tien_dat, addr["xa"]),
        "so_qd_tdc": f"{rng.randint(100, 2999)}/QĐ-UBND",
        "ngay_qd_tdc": ngay_qd + timedelta(days=rng.randint(0, 30)),
    }


def labels(th: dict, nhan_khau: int) -> dict:
    """Nhãn suy luận cho ground_truth.json > compensation: số đúng, không bị ca lỗi sửa."""
    tdc = th["tdc"]
    # Thưởng chỉ đúng khi bàn giao đúng hạn: ca lỗi M17 có quyết định khen thưởng dù trễ hạn, nhãn vẫn là 0.
    thuong = th["tien_thuong"] if th["ban_giao"] == "dung-han" else 0
    support = tdc.get("ho_tro_suat_toi_thieu", 0) + tdc.get("ho_tro_tu_lo", 0)
    return {
        "pham_vi_thu_hoi": th["pham_vi"],
        "dien_tich_thu_hoi": th["dien_tich"],
        "gia_dat": th["gia_dat"],
        "tien_bt_dat": th["tien_bt_dat"],
        "tien_bt_cong_trinh": th["tien_bt_cong_trinh"],
        "ban_giao_dung_han": th["ban_giao"] == "dung-han",
        "tien_thuong": thuong,
        "tai_dinh_cu": {k: tdc[k] for k in ("du_dieu_kien", "hinh_thuc", "so_suat")}
                      | {"nhan_khau": nhan_khau,
                         "tien_phai_nop": tdc.get("tien_phai_nop", 0), "tien_duoc_nhan": tdc.get("tien_duoc_nhan", 0)},
        "tong_bt_ht": th["tien_bt_dat"] + th["tien_bt_cong_trinh"] + thuong + support,
    }
