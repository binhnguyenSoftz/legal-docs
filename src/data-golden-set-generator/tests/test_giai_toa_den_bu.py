"""Thủ tục giải tỏa đền bù: bộ giấy tờ AIP-027 mục 4.2."""

import random
from datetime import date

import pytest

from generator import dossier, people, spec
from generator.fields import address, cccd, money

DOC_TYPES = {"can-cuoc", "giay-chung-tu", "giay-chung-nhan-nha-dat", "ban-ve-hien-trang",
             "to-dang-ky-nha-dat", "so-ho-khau", "giay-sang-dat"}


@pytest.fixture(scope="module")
def proc():
    return spec.load_procedure("giai-toa-den-bu")


@pytest.fixture(scope="module")
def dossiers(proc):
    return [dossier.build(proc, 11, i) for i in range(216)]


@pytest.mark.parametrize("n,words", [
    (0, "Không"), (15, "Mười lăm"), (21, "Hai mươi mốt"), (105, "Một trăm linh năm"),
    (24, "Hai mươi tư"), (1_005_000, "Một triệu không trăm linh năm nghìn"),
    (26_000_000, "Hai mươi sáu triệu"), (250_500_000, "Hai trăm năm mươi triệu năm trăm nghìn"),
])
def test_money_words(n, words):
    assert money.to_words(n) == words


def test_money_format():
    assert money.group(26_000_000) == "26.000.000"
    assert money.decimal(68.5) == "68,5"
    assert money.decimal(7.0) == "7"


def test_mrz_check_digits():
    # Ví dụ ICAO 9303: số giấy tờ L898902C3 -> 6, ngày 740812 -> 2.
    assert cccd._mrz_check("L898902C3") == "6"
    assert cccd._mrz_check("740812") == "2"
    lines = cccd.mrz("001079780971", date(1979, 5, 28), "male", date(2039, 5, 28), "Pham Van Khoa")
    assert [len(x) for x in lines] == [30, 30, 30]
    assert lines[2].startswith("PHAM<<VAN<KHOA")


def test_address_by_date():
    addr = address.generate(random.Random(3))
    assert address.format_at(addr, date(2025, 6, 30)) == address.format_old(addr)
    assert address.format_at(addr, date(2025, 7, 1)) == address.format(addr)
    assert addr["huyen_cu"] in address.format_old(addr)


def test_all_documents_and_reproducible(proc, dossiers):
    assert set(proc.schemas) == DOC_TYPES
    assert dossier.build(proc, 11, 5) == dossiers[5]


def test_every_dossier_has_all_documents(dossiers):
    for d in dossiers:
        assert [x["doc_type"] for x in d["documents"]] == [
            "can-cuoc", "giay-chung-tu", "giay-chung-nhan-nha-dat", "ban-ve-hien-trang",
            "to-dang-ky-nha-dat", "so-ho-khau", "giay-sang-dat"]
        assert d["missing_documents"] == []


def test_coverage_plan_balanced(proc):
    plans = [dossier.plan(proc, i) for i in range(108)]
    assert len({tuple(p.values()) for p in plans}) == 108, "108 hồ sơ đầu phủ hết mọi tổ hợp"
    for dim in proc.coverage:
        counts = [sum(p[dim["name"]] == v for p in plans[:12]) for v in dim["values"]]
        assert max(counts) - min(counts) == 0, f"{dim['name']} lệch trong 12 hồ sơ đầu: {counts}"


def test_profile_matches_documents(proc, dossiers):
    for d in dossiers:
        prof = d["profile"]
        assert prof["variants"] == {x["doc_type"]: x["variant"] for x in d["documents"]}
        expect = dossier.expected_variants(proc, prof["targets"])
        for doc_type, variant in expect.items():
            if doc_type == "can-cuoc" and "the" in prof["unmet"]:
                continue
            if doc_type == "can-cuoc" and d["persona"]["the"]["loai"] == cccd.CMND:
                continue  # Ca lỗi M05 ép CMND, ưu tiên hơn kịch bản
            assert prof["variants"][doc_type] == variant, (d["dossier_id"], doc_type)
        # Chỉ chấp nhận chưa khớp khi không khả thi, đều ở ca M07 (người nộp 15-17 tuổi): không thể có CCCD mã vạch
        # (cấp tới 01/2021), cha mẹ sinh sau 1960 không thể đã mua đất trước 18/12/1980.
        infeasible = {("the", "cccd-ma-vach"), ("nguon_goc", "truoc-18-12-1980")}
        for dim in prof["unmet"]:
            assert (dim, prof["targets"][dim]) in infeasible
            assert d["decision"]["reasons"][0]["mutation"] == "M07"


def test_random_coverage_has_no_targets(proc):
    d = dossier.build(proc, 11, 0, coverage=False)
    assert d["profile"]["targets"] == {} and d["profile"]["attempts"] == 1


def test_timeline_order(dossiers):
    for d in dossiers:
        t, p = d["timeline"], d["people"]
        assert t["ngay_sang"] < t["ngay_dang_ky"] < t["ngay_cap_gcn"] < t["ngay_mat"] < d["submit_date"]
        assert t["ngay_cap_ho_khau"] < t["ngay_mat"]
        assert p["nguoi_mat"]["ngay_sinh"] < p["nguoi_nop"]["ngay_sinh"] <= t["ngay_mat"]
        assert all(c["ho"] == p["nguoi_nop"]["ho"] for c in p["con"])
        assert p["ho_khau"][0] is p["nguoi_mat"]


def test_variants_follow_dates(dossiers):
    seen = set()
    for d in dossiers:
        docs = {x["doc_type"]: x for x in d["documents"]}
        if "giay-chung-tu" in docs:
            ct = docs["giay-chung-tu"]
            assert ct["variant"] == ("giay-chung-tu" if ct["issue_date"] < date(2016, 1, 1) else "trich-luc-khai-tu")
            seen.add(ct["variant"])
        cc = docs["can-cuoc"]
        assert cc["variant"] == d["persona"]["the"]["loai"]
        seen.add(cc["variant"])
        hk = docs["so-ho-khau"]
        assert hk["variant"] == ("da-xoa-ten" if d["timeline"]["ngay_mat"] < date(2023, 1, 1) else "chua-xoa-ten")
        assert hk["groups"]["tv"] == min(10, len(d["people"]["ho_khau"]))
        assert hk["fields"]["tv1_ho_ten"]["value"] == d["people"]["nguoi_mat"]["ho_ten"]
    assert {"giay-chung-tu", "trich-luc-khai-tu", "cccd-chip", "cccd-ma-vach", "cmnd-9"} <= seen


def test_old_documents_use_old_address(dossiers):
    for d in dossiers:
        parts = d["property"]["dia_chi_parts"]
        for x in d["documents"]:
            if any(f["mutated_by"] for f in x["fields"].values()):
                continue  # Ca lỗi M09 cố ý đổi địa chỉ trên bản vẽ
            if x["doc_type"] == "giay-chung-nhan-nha-dat":
                assert x["fields"]["dia_chi_nha"]["value"] == address.format_old(parts)
            if x["doc_type"] == "ban-ve-hien-trang":
                assert x["fields"]["dia_chi"]["value"] == address.format_at(parts, x["issue_date"])


def test_freeform_fields_are_on_page(dossiers):
    for d in dossiers:
        for x in d["documents"]:
            if x["doc_type"] != "giay-sang-dat":
                continue
            used = {s["f"] for b in x["blocks"] for s in b["segments"] if "f" in s}
            used |= {s["field"] for b in x["blocks"] for s in b.get("signers", [])}
            assert set(x["fields"]) == used
            assert {"ben_ban_ho_ten", "ben_mua_ho_ten", "dien_tich", "gia", "ngay_lap"} <= used


def test_labels_match_mutations(dossiers):
    seen, labels_seen = set(), set()
    for d in dossiers:
        label, reasons = d["decision"]["label"], d["decision"]["reasons"]
        labels_seen.add(label)
        if label == "approve":
            assert reasons == [] and d["missing_documents"] == []
            assert all(f["mutated_by"] is None for x in d["documents"] for f in x["fields"].values())
            assert d["persona"]["the"]["loai"] != cccd.CMND
            continue
        m = reasons[0]["mutation"]
        seen.add(m)
        if m == "M05":
            assert d["persona"]["the"]["loai"] == cccd.CMND
        if m == "M04":
            gcn = next(x for x in d["documents"] if x["doc_type"] == "giay-chung-nhan-nha-dat")
            bv = next(x for x in d["documents"] if x["doc_type"] == "ban-ve-hien-trang")
            assert gcn["fields"]["dien_tich"]["value"] != bv["fields"]["dien_tich"]["value"]
    assert seen == {"M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09"}
    assert labels_seen <= {"approve", "request_supplement"}


def test_diversity(dossiers):
    """Tập dữ liệu không được lặp lại một nhóm người, một vài địa chỉ."""
    from generator.fields import dates
    people_all, provinces, wards, ethnic, relations = [], set(), set(), set(), set()
    for d in dossiers:
        p = d["people"]
        people_all += [p["nguoi_mat"], p["vo_chong"], p["ben_ban"], *p["con"]]
        a = d["property"]["dia_chi_parts"]
        provinces.add(a["tinh_cu"])
        wards.add((a["tinh_cu"], a["huyen_cu"], a["xa_cu"]))
        ethnic.add(p["nguoi_nop"]["dan_toc"])
        relations |= {x["quan_he"] for x in p["ho_khau"]}
        hk = next(x for x in d["documents"] if x["doc_type"] == "so-ho-khau")
        for k in range(1, hk["groups"]["tv"] + 1):
            job = hk["fields"][f"tv{k}_nghe_nghiep"]["value"]
            age = dates.age_on(hk["fields"][f"tv{k}_ngay_sinh"]["value"], hk["issue_date"])
            assert not (job == "Học sinh" and age >= 18 or job == "Hưu trí" and age < 60), (job, age)
    names = [x["ho_ten"] for x in people_all]
    assert len(set(names)) / len(names) > 0.8
    assert any(len(n.split()) == 4 for n in names)
    assert len(provinces) >= 40 and len(wards) >= 140
    assert len(ethnic) >= 3
    assert {"Con dâu", "Con rể", "Cháu"} & relations


def test_land_origin_eras(dossiers):
    seen = set()
    for d in dossiers:
        era = people.land_era(d["timeline"]["ngay_sang"])
        seen.add(era)
        if "nguon_goc" not in d["profile"]["unmet"]:
            assert era == d["profile"]["targets"]["nguon_goc"]
        assert d["compensation"]["nguon_goc_dat"] == era
    assert seen == set(people.LAND_ERAS)


def test_compensation_ground_truth(dossiers):
    for d in dossiers:
        c, p = d["compensation"], d["people"]
        assert c["nguoi_dung_ten"] == p["nguoi_mat"]["ho_ten"]
        assert c["nguoi_dai_dien"] == d["persona"]["ho_ten"] in c["nguoi_thua_ke"]
        assert c["dien_tich_dat"] == d["property"]["dien_tich"] and c["so_thua"] == d["property"]["so_thua"]
        assert p["nguoi_mat"]["ho_ten"] not in c["nguoi_thua_ke"]
        assert 1 <= c["nhan_khau"] < len(p["ho_khau"])
