"""Nhóm người có quan hệ trong hồ sơ nhà đất có người đứng tên đã mất (giải tỏa đền bù), kèm dòng thời gian của thửa đất.

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


# Thời điểm bắt đầu sử dụng đất (ngày lập giấy sang đất), theo các mốc xét bồi thường về đất.
# [CẦN XÁC NHẬN] mốc theo Luật Đất đai 2024 (18/12/1980, 15/10/1993); giấy sang đất sinh trong 1976-1998.
LAND_ERAS = {
    "truoc-18-12-1980": (date.min, date(1980, 12, 17)),
    "1980-15-10-1993": (date(1980, 12, 18), date(1993, 10, 14)),
    "tu-15-10-1993": (date(1993, 10, 15), date.max),
}


def land_era(d: date) -> str:
    return next(name for name, (lo, hi) in LAND_ERAS.items() if lo <= d <= hi)


def _between(rng, lo: date, hi: date) -> date:
    return dates.between(rng, lo, max(lo, hi))


def _in_laws(rng: random.Random, con: list[dict], submit: date, home: dict) -> list[dict]:
    """Con dâu, con rể và cháu của 0-2 người con đã lập gia đình, vẫn ở chung hộ khẩu."""
    out = []
    grown = [c for c in con if dates.age_on(c["ngay_sinh"], date(2010, 1, 1)) >= 20]
    for c in rng.sample(grown, min(len(grown), rng.choice([0, 0, 1, 1, 2]))):
        sp_gender = "female" if c["gender"] == "male" else "male"
        sp_dob = _between(rng, dates.add_years(c["ngay_sinh"], -6), dates.add_years(c["ngay_sinh"], 6))
        spouse = persona.make(rng, sp_dob, sp_gender, submit, thuong_tru=home)
        spouse["quan_he"] = "Con dâu" if sp_gender == "female" else "Con rể"
        out.append(spouse)
        grand_ho = c["ho"] if c["gender"] == "male" else spouse["ho"]
        mother = c if c["gender"] == "female" else spouse
        for _ in range(rng.randint(0, 3)):
            lo = dates.add_years(max(c["ngay_sinh"], sp_dob), 20)
            hi = min(dates.add_years(mother["ngay_sinh"], 42), date(2022, 12, 31))
            if lo > hi:
                break
            kid = persona.make(rng, _between(rng, lo, hi), rng.choice(["male", "female"]), submit, ho=grand_ho,
                               thuong_tru=home, dan_toc=c["dan_toc"], ton_giao=c["ton_giao"])
            kid["quan_he"] = "Cháu"
            out.append(kid)
    return out


def build(rng: random.Random, submit: date, applicant: dict, nam_mat: str | None = None,
          nguon_goc: str | None = None) -> dict:
    """applicant: persona người nộp (đã dựng). nam_mat: ép thời kỳ mất (DEATH_ERAS).
    nguon_goc: ép thời điểm bắt đầu sử dụng đất (LAND_ERAS). Trả về people + timeline."""
    app_dob = applicant["ngay_sinh"]
    home = applicant["noi_thuong_tru_parts"]

    # Người đứng tên (cha hoặc mẹ của người nộp) phải đủ 20 tuổi trước khi mua đất (<= 1998).
    dec_gender = rng.choice(["male", "female"])
    dec_dob = _between(rng, dates.add_years(app_dob, -45), min(dates.add_years(app_dob, -18), date(1978, 12, 31)))
    sang_lo, sang_hi = max(dates.add_years(dec_dob, 20), date(1976, 1, 1)), date(1998, 12, 31)
    if nguon_goc:
        era_lo, era_hi = LAND_ERAS[nguon_goc]
        sang_lo, sang_hi = max(sang_lo, era_lo), min(sang_hi, era_hi)
    ngay_sang = _between(rng, sang_lo, sang_hi)
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
    # Cả gia đình cùng dân tộc, tôn giáo với người nộp.
    same = {"dan_toc": applicant["dan_toc"], "ton_giao": applicant["ton_giao"]}
    nguoi_mat = persona.make(rng, dec_dob, dec_gender, ngay_mat, ho=dec_ho, thuong_tru=home, **same)
    nguoi_mat.update({
        "ngay_mat": ngay_mat,
        "gio_mat": f"{rng.randint(0, 23):02d} giờ {rng.randrange(0, 60, 5):02d} phút",
        "noi_mat": rng.choice(DEATH_PLACES),
        "nguyen_nhan": rng.choice(CAUSES),
    })

    sp_gender = "female" if dec_gender == "male" else "male"
    sp_dob = _between(rng, dates.add_years(dec_dob, -8), min(dates.add_years(dec_dob, 8), dates.add_years(app_dob, -18)))
    vo_chong = persona.make(rng, sp_dob, sp_gender, submit, ho=father_ho if sp_gender == "male" else None,
                            thuong_tru=home, **same)
    vo_chong["con_song"] = dates.age_on(sp_dob, submit) < 95 and rng.random() < 0.7

    # Thế hệ trước đông con hơn.
    extra = rng.randint(1, 7) if dec_dob.year < 1950 else rng.randint(0, 5) if dec_dob.year < 1965 else rng.randint(0, 3)
    con = [applicant]
    for _ in range(extra):
        mother_dob = dec_dob if dec_gender == "female" else sp_dob
        lo = dates.add_years(max(dec_dob, sp_dob), 18)
        hi = min(dates.add_years(mother_dob, 45), ngay_mat, submit - timedelta(days=1))
        dob = _between(rng, lo, hi)
        child = persona.make(rng, dob, rng.choice(["male", "female"]), submit, ho=family_ho, thuong_tru=home, **same)
        con.append(child)
    con.sort(key=lambda p: p["ngay_sinh"])
    for c in con:
        c["quan_he"] = "Con"

    nguoi_mat["quan_he"] = "Chủ hộ"
    vo_chong["quan_he"] = "Vợ" if sp_gender == "female" else "Chồng"
    ho_khau = [nguoi_mat, vo_chong] + [c for c in con if c["ngay_sinh"] <= date(2022, 12, 31)]
    ho_khau += _in_laws(rng, con, submit, home)

    seller_dob = _between(rng, dates.add_years(ngay_sang, -70), dates.add_years(ngay_sang, -25))
    seller_as_of = ngay_sang + timedelta(days=1)
    ben_ban = persona.make(rng, seller_dob, rng.choice(["male", "female"]), seller_as_of)
    # Vợ/chồng bên bán cùng ký giấy sang đất (không phải lúc nào cũng có).
    bb_sp_gender = "female" if ben_ban["gender"] == "male" else "male"
    bb_sp_dob = _between(rng, dates.add_years(seller_dob, -6), dates.add_years(seller_dob, 6))
    ben_ban_vc = persona.make(rng, bb_sp_dob, bb_sp_gender, seller_as_of, thuong_tru=ben_ban["noi_thuong_tru_parts"],
                              dan_toc=ben_ban["dan_toc"], ton_giao=ben_ban["ton_giao"])
    ben_ban_vc["quan_he"] = "Vợ" if bb_sp_gender == "female" else "Chồng"
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
            "ben_ban_vc": ben_ban_vc,
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


def compensation(fam: dict, prop: dict, submit: date) -> dict:
    """Thông tin để lập phương án bồi thường: nhãn cho đánh giá cuối (AIP-027), tính từ dữ liệu đúng, không bị ca lỗi sửa.

    [CẦN XÁC NHẬN] Người thừa kế lấy theo hàng thừa kế thứ nhất (vợ/chồng còn sống, các con), chưa xét di chúc.
    """
    p, t = fam["people"], fam["timeline"]
    heirs = ([p["vo_chong"]] if p["vo_chong"].get("con_song") else []) + p["con"]
    alive = [x for x in p["ho_khau"] if x is not p["nguoi_mat"] and (x is not p["vo_chong"] or x.get("con_song"))]
    return {
        "nguoi_dung_ten": p["nguoi_mat"]["ho_ten"],
        "nguoi_dai_dien": p["nguoi_nop"]["ho_ten"],
        "nguoi_thua_ke": [x["ho_ten"] for x in heirs],
        "ngay_bat_dau_su_dung_dat": t["ngay_sang"],
        "nguon_goc_dat": land_era(t["ngay_sang"]),
        "so_thua": prop["so_thua"],
        "to_ban_do": prop["to_ban_do"],
        "dien_tich_dat": prop["dien_tich"],
        "dien_tich_xay_dung": prop["nha"]["dien_tich_xay_dung"],
        "dien_tich_san": prop["nha"]["dien_tich_san"],
        "so_tang": prop["nha"]["so_tang"],
        "ket_cau": prop["nha"]["ket_cau"],
        "nhan_khau": len(alive),
    }
