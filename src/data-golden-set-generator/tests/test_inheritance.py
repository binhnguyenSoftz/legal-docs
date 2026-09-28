"""Thủ tục thừa kế nhà đất: bộ giấy tờ AIP-027 mục 4.2."""

import random
from datetime import date

import pytest

from generator import dossier, spec
from generator.fields import address, cccd, money

DOC_TYPES = {"can-cuoc", "giay-chung-tu", "giay-chung-nhan-nha-dat", "ban-ve-hien-trang",
             "to-dang-ky-nha-dat", "so-ho-khau", "giay-sang-dat"}


@pytest.fixture(scope="module")
def proc():
    return spec.load_procedure("thua-ke-nha-dat")


@pytest.fixture(scope="module")
def dossiers(proc):
    return [dossier.build(proc, 11, i) for i in range(150)]


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
    plans = [dossier.plan(proc, i) for i in range(36)]
    assert len({tuple(p.values()) for p in plans}) == 36, "36 hồ sơ đầu phủ hết mọi tổ hợp"
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
        # Chỉ chấp nhận chưa khớp khi không khả thi: người nộp dưới 18 không thể có CCCD mã vạch (cấp tới 01/2021).
        for dim in prof["unmet"]:
            assert dim == "the" and prof["targets"]["the"] == "cccd-ma-vach"
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
        assert hk["groups"]["tv"] == min(6, len(d["people"]["ho_khau"]))
        assert hk["fields"]["tv1_ho_ten"]["value"] == d["people"]["nguoi_mat"]["ho_ten"]
    assert {"giay-chung-tu", "trich-luc-khai-tu", "cccd-chip", "cccd-ma-vach", "cmnd-9"} <= seen


def test_old_documents_use_old_address(dossiers):
    for d in dossiers:
        parts = d["property"]["dia_chi_parts"]
        for x in d["documents"]:
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
    seen = set()
    for d in dossiers:
        label, reasons = d["decision"]["label"], d["decision"]["reasons"]
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
    assert seen == {"M02", "M03", "M04", "M05", "M06", "M07"}
