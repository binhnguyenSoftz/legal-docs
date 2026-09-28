"""Nhóm người có quan hệ trong một hồ sơ thừa kế nhà đất, kèm dòng thời gian của thửa đất.

Dòng thời gian (bảo đảm thứ tự để hồ sơ hợp lệ không tự mâu thuẫn):
  mua đất bằng giấy tay (ngay_sang) -> tờ đăng ký nhà đất (ngay_dang_ky) -> sổ hộ khẩu (ngay_cap_ho_khau)
  -> giấy chứng nhận (ngay_cap_gcn) -> người đứng tên mất (ngay_mat) -> nộp hồ sơ.

`persona` của hồ sơ là người nộp, một trong các con.
"""

import random
from datetime import date, timedelta

from generator import persona
from generator.fields import dates

CAUSES = ["Bệnh", "Già yếu", "Bệnh tim", "Tai biến mạch máu não", "Ung thư"]
DEATH_PLACES = ["Tại nhà riêng", "Tại nhà riêng", "Tại bệnh viện"]


# Thời kỳ người đứng tên mất, quyết định mẫu giấy chứng tử (trước/sau Luật Hộ tịch 2016)
# và sổ hộ khẩu có dòng xóa tên hay không (sổ hết giá trị từ 2023). Giấy chứng tử cấp trong 15 ngày sau khi mất.
DEATH_ERAS = {
    "truoc-2016": (date.min, date(2015, 12, 15)),
    "2016-2022": (date(2016, 1, 1), date(2022, 12, 31)),
    "tu-2023": (date(2023, 1, 1), date.max),
}


def _between(rng, lo: date, hi: date) -> date:
    return dates.between(rng, lo, max(lo, hi))


def build(rng: random.Random, submit: date, applicant: dict, nam_mat: str | None = None) -> dict:
    """applicant: persona người nộp (đã dựng). nam_mat: ép thời kỳ mất (DEATH_ERAS). Trả về people + timeline."""
    app_dob = applicant["ngay_sinh"]
    home = applicant["noi_thuong_tru_parts"]

    # Người đứng tên (cha hoặc mẹ của người nộp) phải đủ 20 tuổi trước khi mua đất (<= 1998).
    dec_gender = rng.choice(["male", "female"])
    dec_dob = _between(rng, dates.add_years(app_dob, -45), min(dates.add_years(app_dob, -18), date(1978, 12, 31)))
    ngay_sang = _between(rng, max(dates.add_years(dec_dob, 20), date(1976, 1, 1)), date(1998, 12, 31))
    ngay_dang_ky = _between(rng, max(ngay_sang + timedelta(days=30), date(1990, 1, 1)), date(2000, 12, 31))
    ngay_cap_ho_khau = _between(rng, max(ngay_sang, date(1990, 1, 1)), date(2008, 12, 31))
    ngay_cap_gcn = _between(rng, max(ngay_dang_ky + timedelta(days=60), date(1995, 1, 1)), date(2008, 12, 31))
    death_lo = max(ngay_cap_gcn + timedelta(days=365), dates.add_years(dec_dob, 35),
                   dates.add_years(submit, -25), app_dob + timedelta(days=1), ngay_cap_ho_khau + timedelta(days=1))
    death_hi = min(submit - timedelta(days=30), dates.add_years(dec_dob, 99))
    if nam_mat:
        era_lo, era_hi = DEATH_ERAS[nam_mat]
        death_lo, death_hi = max(death_lo, era_lo), min(death_hi, era_hi)
    ngay_mat = _between(rng, death_lo, death_hi)

    # Họ của con theo họ cha.
    family_ho = applicant["ho"]
    father_ho = family_ho
    dec_ho = family_ho if dec_gender == "male" else None
    nguoi_mat = persona.make(rng, dec_dob, dec_gender, ngay_mat, ho=dec_ho, thuong_tru=home)
    nguoi_mat.update({
        "ngay_mat": ngay_mat,
        "gio_mat": f"{rng.randint(0, 23):02d} giờ {rng.randrange(0, 60, 5):02d} phút",
        "noi_mat": rng.choice(DEATH_PLACES),
        "nguyen_nhan": rng.choice(CAUSES),
    })

    sp_gender = "female" if dec_gender == "male" else "male"
    sp_dob = _between(rng, dates.add_years(dec_dob, -8), min(dates.add_years(dec_dob, 8), dates.add_years(app_dob, -18)))
    vo_chong = persona.make(rng, sp_dob, sp_gender, submit, ho=father_ho if sp_gender == "male" else None, thuong_tru=home)
    vo_chong["con_song"] = dates.age_on(sp_dob, submit) < 95 and rng.random() < 0.7

    con = [applicant]
    for _ in range(rng.randint(0, 3)):
        mother_dob = dec_dob if dec_gender == "female" else sp_dob
        lo = dates.add_years(max(dec_dob, sp_dob), 18)
        hi = min(dates.add_years(mother_dob, 45), ngay_mat, submit - timedelta(days=1))
        dob = _between(rng, lo, hi)
        child = persona.make(rng, dob, rng.choice(["male", "female"]), submit, ho=family_ho, thuong_tru=home)
        con.append(child)
    con.sort(key=lambda p: p["ngay_sinh"])
    for c in con:
        c["quan_he"] = "Con"

    nguoi_mat["quan_he"] = "Chủ hộ"
    vo_chong["quan_he"] = "Vợ" if sp_gender == "female" else "Chồng"
    ho_khau = [nguoi_mat, vo_chong] + [c for c in con if c["ngay_sinh"] <= date(2022, 12, 31)]

    seller_dob = _between(rng, dates.add_years(ngay_sang, -70), dates.add_years(ngay_sang, -25))
    seller_as_of = ngay_sang + timedelta(days=1)
    ben_ban = persona.make(rng, seller_dob, rng.choice(["male", "female"]), seller_as_of)
    witness_dob = _between(rng, dates.add_years(ngay_sang, -65), dates.add_years(ngay_sang, -25))
    lam_chung = persona.make(rng, witness_dob, rng.choice(["male", "female"]), seller_as_of, thuong_tru=home)

    return {
        "people": {
            "nguoi_nop": applicant,
            "nguoi_mat": nguoi_mat,
            "vo_chong": vo_chong,
            "con": con,
            "ho_khau": ho_khau,
            "ben_ban": ben_ban,
            "lam_chung": lam_chung,
        },
        "timeline": {
            "ngay_sang": ngay_sang,
            "ngay_dang_ky": ngay_dang_ky,
            "ngay_cap_ho_khau": ngay_cap_ho_khau,
            "ngay_cap_gcn": ngay_cap_gcn,
            "ngay_mat": ngay_mat,
        },
    }
