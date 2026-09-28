"""Một người trong hồ sơ. `build` dựng người nộp; `make` dựng người bất kỳ (kể cả người đã mất) cho people.py."""

import random
from datetime import date, timedelta

from generator.fields import address, cccd, dates, names, phone

RELIGIONS = ["Không", "Không", "Không", "Không", "Phật giáo", "Công giáo"]


def _ca(province: str) -> str:
    """Nơi cấp CMND: 'CA TP. Hà Nội', 'CA Quảng Nam'."""
    return "CA " + province.replace("Thành phố ", "TP. ").replace("Tỉnh ", "")


def _cards(rng: random.Random, dob: date, gender: str, as_of: date, number: str, thuong_tru: dict,
           card: str | None) -> dict:
    """CMND cũ (nếu có) và thẻ đang dùng tại as_of.

    card: ép thế hệ thẻ đang dùng. 'cmnd-9': dùng CMND; 'cccd-ma-vach' | 'cccd-chip' | 'the-can-cuoc': cấp trong
    khoảng của thế hệ đó. Không khả thi với ngày sinh này (thẻ đã hết hạn) thì sinh như bình thường.
    """
    out = {"cmnd": None, "ngay_cap_cmnd": None, "noi_cap_cmnd": None,
           "ngay_cap_cccd": None, "cccd_het_han": None, "noi_cap_cccd": None}
    cmnd_issue = cccd.cmnd_issue_date(rng, dob, as_of - timedelta(days=1))
    if cmnd_issue:
        out.update(cmnd=cccd.cmnd_generate(rng, thuong_tru["tinh_cu"]), ngay_cap_cmnd=cmnd_issue,
                   noi_cap_cmnd=_ca(thuong_tru["tinh_cu"]))
    cccd_issue = None
    if as_of > cccd.EARLIEST_ISSUE:
        if card and card != cccd.CMND:
            cccd_issue = cccd.issue_date(rng, dob, as_of, cccd.generation_window(card))
        cccd_issue = cccd_issue or cccd.issue_date(rng, dob, as_of)
    if cccd_issue:
        kind, place = cccd.generation(cccd_issue)
        out.update(ngay_cap_cccd=cccd_issue, cccd_het_han=cccd.expiry_date(dob, cccd_issue), noi_cap_cccd=place)

    if (card == cccd.CMND or not cccd_issue) and cmnd_issue:
        the = {"loai": cccd.CMND, "so": out["cmnd"], "ngay_cap": cmnd_issue,
               "ngay_het_han": dates.add_years(cmnd_issue, cccd.CMND_YEARS), "noi_cap": out["noi_cap_cmnd"]}
    elif cccd_issue:
        the = {"loai": kind, "so": number, "ngay_cap": cccd_issue,
               "ngay_het_han": out["cccd_het_han"], "noi_cap": place}
    else:
        the = None
    if the:
        the["dac_diem"] = rng.choice(cccd.IDENTIFYING_MARKS)
    out["the"] = the
    return out


def make(rng: random.Random, dob: date, gender: str, as_of: date, ho: str | None = None,
         card: str | None = None, thuong_tru: dict | None = None) -> dict:
    """as_of: ngày giấy tờ tùy thân phải còn hạn (ngày nộp, hoặc ngày mất với người đã mất)."""
    que_quan = address.generate(rng)
    thuong_tru = thuong_tru or address.generate(rng)
    name = names.generate(rng, gender, ho)
    number = cccd.generate(rng, dob, gender, cccd.code_for(que_quan["tinh_cu"]))
    person = {
        **name,
        "ho_ten_ascii": names.ascii_fold(name["ho_ten"]),
        "gender": gender,
        "gioi_tinh": "Nữ" if gender == "female" else "Nam",
        "xung_ho": "bà" if gender == "female" else "ông",
        "ngay_sinh": dob,
        "cccd": number,
        "noi_thuong_tru": address.format(thuong_tru),
        "noi_thuong_tru_cu": address.format_old(thuong_tru),
        "noi_thuong_tru_parts": thuong_tru,
        "que_quan_parts": que_quan,
        "dien_thoai": phone.generate(rng),
        "dan_toc": "Kinh",
        "ton_giao": rng.choice(RELIGIONS),
        "quoc_tich": "Việt Nam",
    }
    person.update(_cards(rng, dob, gender, as_of, number, thuong_tru, card))
    if person["the"] and person["the"]["loai"] in ("cccd-chip", "the-can-cuoc"):
        person["the"]["mrz"] = cccd.mrz(number, dob, gender, person["the"]["ngay_het_han"], person["ho_ten_ascii"])
    return person


def build(rng: random.Random, as_of: date, age: tuple[int, int] = (18, 70), gender: str = "any",
          card: str | None = None, ho: str | None = None) -> dict:
    if gender == "any":
        gender = rng.choice(["male", "female"])
    dob = dates.dob_for_age(rng, age[0], age[1], as_of)
    return make(rng, dob, gender, as_of, ho=ho, card=card)
