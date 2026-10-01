"""Thủ tục giai-toa-den-bu-tphcm: 7 giấy tờ đầu vào + 5 giấy tờ bồi thường, quy định TP.HCM."""

from collections import Counter

import pytest

from generator import dossier, spec, thu_hoi
from generator.fields import money

HCM = "Thành phố Hồ Chí Minh"
INPUT_DOCS = ["can-cuoc", "giay-chung-tu", "giay-chung-nhan-nha-dat", "ban-ve-hien-trang",
              "to-dang-ky-nha-dat", "so-ho-khau", "giay-sang-dat"]
NEW_MUTATIONS = {f"M{i}" for i in range(10, 20)}


@pytest.fixture(scope="module")
def proc():
    return spec.load_procedure("giai-toa-den-bu-tphcm")


@pytest.fixture(scope="module")
def dossiers(proc):
    return [dossier.build(proc, 13, i) for i in range(400)]


def _docs(d):
    return {x["doc_type"]: x for x in d["documents"]}


def _v(doc, name):
    return doc["fields"][name]["value"]


def _row_ok(doc, prefix, i):
    """Một dòng bảng chiết tính đúng công thức."""
    p = f"{prefix}{i}_"
    if prefix == "d":
        return _v(doc, p + "thanh_tien") == round(_v(doc, p + "dien_tich") * _v(doc, p + "don_gia") * _v(doc, p + "ty_le") / 100)
    new_value = round(_v(doc, p + "khoi_luong") * _v(doc, p + "don_gia"))
    current = round(new_value * _v(doc, p + "ty_le") / 100)
    extra = max(0, round(new_value * thu_hoi.FLOOR_RATE / 100) - current)
    return (_v(doc, p + "gia_tri_hien_co") == current and _v(doc, p + "bo_sung") == extra
            and _v(doc, p + "thanh_tien") == current + extra)


def _table_ok(doc, prefix):
    n = doc["groups"][prefix]
    rows = all(_row_ok(doc, prefix, i) for i in range(1, n + 1))
    total = sum(_v(doc, f"{prefix}{i}_thanh_tien") for i in range(1, n + 1))
    words = doc["fields"]["tong_bang_chu"]["text"] == money.to_words(_v(doc, "tong_cong")) + " đồng"
    return rows and total == _v(doc, "tong_cong") and words


def test_documents_shared_and_reproducible(proc, dossiers):
    assert proc.schemas["can-cuoc"].procedure == "giai-toa-den-bu"
    assert proc.schemas["bt-dat"].template == "giai-toa-den-bu-tphcm/bt-dat/template.html.j2"
    assert dossier.build(proc, 13, 7) == dossiers[7]


def test_conditional_documents(dossiers):
    """Tái định cư, khen thưởng chỉ có khi đủ điều kiện; không có thì không phải thiếu giấy tờ."""
    for d in dossiers:
        th, docs = d["thu_hoi"], _docs(d)
        assert [x["doc_type"] for x in d["documents"]][:10] == INPUT_DOCS + ["gxn-1131", "bt-dat", "bt-cong-trinh"]
        assert d["missing_documents"] == []
        assert ("tai-dinh-cu" in docs) == th["tdc"]["du_dieu_kien"]
        assert th["tdc"]["du_dieu_kien"] == (th["khong_du_o"] and not th["co_cho_o_khac"])
        assert ("khen-thuong" in docs) == th["co_khen_thuong"]
        if "tai-dinh-cu" in docs:
            assert docs["tai-dinh-cu"]["variant"] == th["tdc"]["hinh_thuc"]


def test_everything_in_hcmc(dossiers):
    for d in dossiers:
        assert d["property"]["dia_chi_parts"]["tinh"] == HCM
        assert d["people"]["nguoi_mat"]["noi_thuong_tru_parts"]["tinh"] == HCM


def test_coverage_balanced(proc, dossiers):
    plans = [dossier.plan(proc, i) for i in range(16)]
    assert len({(p["pham_vi"], p["ban_giao"], p["tdc"]) for p in plans}) == 16, "16 hồ sơ đầu phủ mọi tình huống bồi thường"
    for d in dossiers:
        for dim in ("pham_vi", "ban_giao", "tdc"):
            assert dim not in d["profile"]["unmet"]


def test_timeline(dossiers):
    for d in dossiers:
        th = d["thu_hoi"]
        assert d["submit_date"] < th["ngay_gxn"] < th["ngay_qd"] <= th["ngay_qd_tdc"]
        assert th["ngay_qd"] >= thu_hoi.EFFECTIVE
        assert th["ngay_qd"] < th["ngay_ban_giao"] < th["ngay_qd_thuong"]
        assert (th["ngay_ban_giao"] <= th["han_ban_giao"]) == (th["ban_giao"] == "dung-han")


def test_valid_dossiers_follow_formulas(dossiers):
    for d in dossiers:
        if d["decision"]["label"] != "approve":
            continue
        th, docs, c = d["thu_hoi"], _docs(d), d["compensation"]
        bt, ct = docs["bt-dat"], docs["bt-cong-trinh"]
        assert _table_ok(bt, "d") and _table_ok(ct, "ct")
        assert _v(bt, "tong_cong") == c["tien_bt_dat"] and _v(ct, "tong_cong") == c["tien_bt_cong_trinh"]
        assert sum(_v(bt, f"d{i}_dien_tich") for i in range(1, bt["groups"]["d"] + 1)) <= _v(bt, "dien_tich_thu_hoi")
        assert _v(bt, "dien_tich_thu_hoi") <= d["property"]["dien_tich"]
        assert _v(docs["gxn-1131"], "thoi_diem_su_dung") == d["timeline"]["ngay_sang"]
        if "khen-thuong" in docs:
            cap = thu_hoi.REWARD_FULL_CAP if th["pham_vi"] == "toan-bo" else thu_hoi.REWARD_PART_CAP
            assert _v(docs["khen-thuong"], "so_tien") == c["tien_thuong"] <= cap
        else:
            assert c["tien_thuong"] == 0
        if "tai-dinh-cu" in docs:
            tdc = docs["tai-dinh-cu"]
            assert _v(tdc, "so_nhan_khau") == c["nhan_khau"]
            support = max(0, _v(tdc, "gia_suat_toi_thieu") - c["tien_bt_dat"])
            assert _v(tdc, "ho_tro_suat_toi_thieu") == support
            if tdc["variant"] != "tu-lo-cho-o":
                diff = _v(tdc, "gia_tdc") - c["tien_bt_dat"] - support
                assert _v(tdc, "tien_phai_nop") - _v(tdc, "tien_duoc_nhan") == diff


def test_house_floor_and_partial(dossiers):
    """Bổ sung lên 60% xuất hiện ở cả hai chiều; thu hồi một phần mà phần còn lại không đủ ở thì tính cả căn."""
    floors = Counter()
    for d in dossiers:
        th = d["thu_hoi"]
        house = th["cong_trinh"][0]
        floors[house["bo_sung"] > 0] += 1
        full = th["pham_vi"] == "toan-bo" or th["khong_du_o"]
        assert (house["khoi_luong"] == d["property"]["nha"]["dien_tich_san"]) or not full
    assert floors[True] and floors[False]


def test_mutations_are_detectable(dossiers):
    """Mỗi ca lỗi mới đổi đúng chỗ, và kiểm tra theo quy tắc bắt được."""
    seen = set()
    for d in dossiers:
        reasons = d["decision"]["reasons"]
        if not reasons or reasons[0]["mutation"] not in NEW_MUTATIONS:
            continue
        m = reasons[0]["mutation"]
        seen.add(m)
        th, docs = d["thu_hoi"], _docs(d)
        match m:
            case "M10":
                assert _v(docs["gxn-1131"], "thoi_diem_su_dung") != d["timeline"]["ngay_sang"]
            case "M11":
                assert _v(docs["bt-dat"], "chu_su_dung") != d["people"]["nguoi_mat"]["ho_ten"]
            case "M12" | "M13" | "M14":
                assert not _table_ok(docs["bt-dat"], "d") or m == "M14"
                if m == "M14":
                    assert _v(docs["bt-dat"], "d1_dien_tich") > _v(docs["bt-dat"], "dien_tich_thu_hoi")
            case "M15":
                assert not _table_ok(docs["bt-cong-trinh"], "ct")
            case "M16":
                assert _v(docs["khen-thuong"], "so_tien") > thu_hoi.REWARD_FULL_CAP
                assert docs["khen-thuong"]["fields"]["so_tien_bang_chu"]["mutated_by"] == "M16"
            case "M17":
                k = docs["khen-thuong"]
                assert _v(k, "ngay_ban_giao") > _v(k, "han_ban_giao")
                assert d["compensation"]["tien_thuong"] == 0
            case "M18":
                assert _v(docs["tai-dinh-cu"], "so_nhan_khau") != d["compensation"]["nhan_khau"]
            case "M19":
                assert _v(docs["bt-dat"], "ngay_lap") < th["ngay_gxn"]
        assert d["decision"]["label"] == "request_supplement"
    assert seen == NEW_MUTATIONS
