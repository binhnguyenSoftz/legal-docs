import random
from datetime import date

import pytest

from generator import persona
from generator.fields import cccd, dates, phone


@pytest.mark.parametrize("dob,gender,digit", [
    (date(1990, 5, 1), "male", 0),
    (date(1990, 5, 1), "female", 1),
    (date(2005, 5, 1), "male", 2),
    (date(2005, 5, 1), "female", 3),
])
def test_cccd_century_gender(dob, gender, digit):
    number = cccd.generate(random.Random(1), dob, gender)
    assert number[3] == str(digit)
    assert number[4:6] == f"{dob.year % 100:02d}"
    assert cccd.validate(number, dob, gender) == []


@pytest.mark.parametrize("dob,issued,expected", [
    (date(2000, 3, 10), date(2021, 6, 1), date(2025, 3, 10)),    # 21 tuổi -> hạn tới 25
    (date(2000, 3, 10), date(2023, 6, 1), date(2040, 3, 10)),    # trong 2 năm trước 25 -> tới 40
    (date(1970, 3, 10), date(2022, 1, 1), date(2030, 3, 10)),    # 51 tuổi -> tới 60
    (date(1964, 3, 10), date(2022, 6, 1), None),                  # 58 tuổi -> không thời hạn
])
def test_cccd_expiry(dob, issued, expected):
    assert cccd.expiry_date(dob, issued) == expected


def test_persona_consistent():
    as_of = date(2026, 1, 15)
    for seed in range(200):
        p = persona.build(random.Random(seed), as_of, age=(18, 70))
        assert 18 <= dates.age_on(p["ngay_sinh"], as_of) <= 70
        assert cccd.validate(p["cccd"], p["ngay_sinh"], p["gender"]) == []
        assert p["ngay_cap_cccd"] < as_of
        assert dates.age_on(p["ngay_sinh"], p["ngay_cap_cccd"]) >= 14
        assert p["cccd_het_han"] is None or p["cccd_het_han"] > as_of, "thẻ phải còn hạn ở ca hợp lệ"
        assert phone.validate(p["dien_thoai"]) == []
