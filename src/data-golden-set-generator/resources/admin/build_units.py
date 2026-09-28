"""Dựng units_pre2025.csv, units_2025.csv, cccd_province_codes.csv từ dữ liệu mở.

Nguồn (giấy phép MIT): https://github.com/thanglequoc/vietnamese-provinces-database
- Tag v2.4.1, json/simplified_json_generated_data_vn_units.json: 63 tỉnh, huyện, xã trước 01/7/2025.
- master, dataset-generation-scripts/sapnhap-bando-crawler/sapnhapbando_geo_objects.sql: mỗi xã mới
  kèm cột truocsapnhap liệt kê các xã cũ (lấy từ sapnhap.bando.com.vn).

Ghép: xã cũ trong truocsapnhap được tìm theo tên trong các tỉnh cũ của tỉnh mới. Tên trùng trong cùng tỉnh
(ví dụ "Phường 1" ở nhiều quận) thì dùng gợi ý trong ngoặc "(thị xã ...)"; vẫn trùng thì bỏ, không đoán.

Chạy lại khi nguồn cập nhật:  python resources/admin/build_units.py
"""

import csv
import json
import re
import unicodedata
import urllib.request
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
BASE = "https://raw.githubusercontent.com/thanglequoc/vietnamese-provinces-database"
OLD_URL = f"{BASE}/v2.4.1/json/simplified_json_generated_data_vn_units.json"
NEW_URL = f"{BASE}/master/json/simplified_json_generated_data_vn_units.json"
MERGE_URL = f"{BASE}/master/dataset-generation-scripts/sapnhap-bando-crawler/sapnhapbando_geo_objects.sql"
ROW = re.compile(r"^\s*\('([^']*)', '([^']*)', (?:'([^']*)'|NULL), '[^']*', '([^']*)'", re.M)


def fetch(url: str) -> str:
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read().decode("utf-8")


def norm(s: str) -> str:
    """So khớp tên không phụ thuộc cách bỏ dấu (Hòa/Hoà), hoa thường, khoảng trắng."""
    s = unicodedata.normalize("NFC", s).lower().strip()
    for a, b in (("oà", "òa"), ("oá", "óa"), ("oả", "ỏa"), ("oã", "õa"), ("oạ", "ọa"),
                 ("uỳ", "ùy"), ("uý", "úy"), ("uỷ", "ủy"), ("uỹ", "ũy"), ("uỵ", "ụy")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s)


def main():
    old = json.loads(fetch(OLD_URL))
    new = json.loads(fetch(NEW_URL))
    merge = fetch(MERGE_URL)

    old_by_code, old_prov_of = {}, {}
    for p in old:
        for d in p["District"] or []:
            for w in d["Ward"] or []:
                old_by_code[w["Code"]] = (p["FullName"], d["FullName"], w["FullName"])
                old_prov_of[w["Code"]] = p["Code"]
    new_ward = {}
    for p in new:
        for w in p["Wards"]:
            new_ward[w["Code"]] = (p["FullName"], w["FullName"], p["Code"])

    # Tỉnh cũ thuộc tỉnh mới: mã xã mới là mã của một xã cũ (mã thống kê giữ lại).
    old_provs = defaultdict(set)
    for code, (_, _, pcode) in new_ward.items():
        if code in old_prov_of:
            old_provs[pcode].add(old_prov_of[code])
    index = defaultdict(list)  # (mã tỉnh cũ, tên xã chuẩn hóa) -> [(tỉnh, huyện, xã)]
    for code, (prov, dist, ward) in old_by_code.items():
        index[(old_prov_of[code], norm(ward))].append((prov, dist, ward))

    rows, skipped = [], 0
    for code, name, pcode, before in ROW.findall(merge):
        if not pcode or code not in new_ward:
            continue
        new_prov, new_name, _ = new_ward[code]
        for item in re.split(r",\s*(?![^()]*\))", before):
            item = item.strip()
            m = re.match(r"(.+?)\s*\((.*)\)\s*$", item)
            ward, hint = (m.group(1), m.group(2)) if m else (item, "")
            ward = re.sub(r"\s*phần\s*$", "", ward).strip()
            cands = [c for op in old_provs[pcode] for c in index[(op, norm(ward))]]
            if len(cands) > 1 and hint:
                h = norm(re.sub(r"^(phần|một phần)\s*", "", hint))
                cands = [c for c in cands if h and (h in norm(c[1]) or norm(c[1]).endswith(h.split()[-1]))] or cands
            if len(cands) != 1:
                skipped += 1
                continue
            prov, dist, w = cands[0]
            rows.append({"province": prov, "district": dist, "ward": w,
                         "new_province": new_prov, "new_commune": new_name})

    rows = sorted({tuple(r.values()): r for r in rows}.values(), key=lambda r: tuple(r.values()))
    with open(HERE / "units_pre2025.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with open(HERE / "units_2025.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["province", "commune"])
        writer.writerows(sorted({(p, w) for p, w, _ in new_ward.values()}))
    # Mã tỉnh trong số CCCD = mã thống kê 2 số của tỉnh cũ, thêm 0 đằng trước (Thông tư 59/2021/TT-BCA).
    prefixes = {}
    prev = HERE / "cccd_province_codes.csv"
    if prev.exists():
        with open(prev, encoding="utf-8") as f:
            prefixes = {r["code"]: r.get("cmnd_prefix", "") for r in csv.DictReader(f)}
    with open(prev, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["code", "province", "cmnd_prefix"])
        for p in old:
            code = "0" + p["Code"]
            writer.writerow([code, p["FullName"], prefixes.get(code, "")])
    print(f"units_pre2025.csv: {len(rows)} dòng, bỏ {skipped} xã cũ không xác định được; "
          f"units_2025.csv: {len(new_ward)} xã; cccd_province_codes.csv: {len(old)} tỉnh")


if __name__ == "__main__":
    main()
