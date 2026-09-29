"""Giấy tờ không có mẫu (giấy sang đất viết tay): sinh bố cục và lời văn tự do quanh các trường có cấu trúc.

Trường có cấu trúc (họ tên, diện tích, số tiền, ngày) vẫn do generator quy tắc sinh trong schema.yaml.
Ở đây chỉ ghép lời văn: mỗi câu là một chuỗi có chỗ trống `{ten_truong}`. Câu nào chứa trường
bị bỏ trống thì bỏ cả câu, để văn bản không có chỗ trống lạ.

Kết quả là doc["blocks"]: danh sách khối {kind, align, segments}, segment là
{"t": chữ} hoặc {"f": tên trường}. Template chỉ việc duyệt blocks.

[CẦN BỔ SUNG] Khi nối LLM: sinh thêm câu mẫu theo lô (vẫn dùng chỗ trống `{ten_truong}`, không chứa
giá trị thật), cache ở generated/_llm_cache/ theo seed, rồi trộn vào PHRASES. Parser bên dưới dùng chung.
"""

import random
import re

PLACEHOLDER = re.compile(r"\{(\w+)\}")

PHRASES = {
    "title": ["GIẤY SANG ĐẤT", "GIẤY SANG NHƯỢNG ĐẤT", "GIẤY MUA BÁN ĐẤT", "GIẤY BÁN ĐẤT THỔ CƯ",
              "GIẤY THỎA THUẬN SANG NHƯỢNG NHÀ ĐẤT", "TỜ SANG NHƯỢNG ĐẤT"],
    "place_date": ["{noi_lap}, {ngay_lap}", "Hôm nay, {ngay_lap}"],
    "intro": ["Hôm nay, {ngay_lap}, tại {dia_chi_dat}, chúng tôi gồm có:",
              "Chúng tôi gồm có:", "Hai bên chúng tôi gồm:"],
    "seller_list": [["Bên sang (bên A): {ben_ban_goi} {ben_ban_ho_ten}", "sinh năm {ben_ban_nam_sinh}"],
                    ["Người bán: {ben_ban_goi} {ben_ban_ho_ten}", "năm sinh {ben_ban_nam_sinh}"]],
    "buyer_list": [["Bên nhận sang (bên B): {ben_mua_goi} {ben_mua_ho_ten}", "sinh năm {ben_mua_nam_sinh}"],
                   ["Người mua: {ben_mua_goi} {ben_mua_ho_ten}", "năm sinh {ben_mua_nam_sinh}"]],
    "id": ["CMND số {cmnd}", "số CMND: {cmnd}"],
    "addr": ["Địa chỉ: {dia_chi}", "Hiện ngụ tại: {dia_chi}", "Thường trú tại: {dia_chi}"],
    "narrative_seller": ["Tôi tên là {ben_ban_ho_ten}, sinh năm {ben_ban_nam_sinh}, hiện ngụ tại {ben_ban_dia_chi}.",
                         "Tôi là {ben_ban_ho_ten}, sinh năm {ben_ban_nam_sinh}, cư ngụ tại {ben_ban_dia_chi}."],
    "seller_spouse": ["Cùng {ben_ban_vc_quan_he} tôi là {ben_ban_vc_ho_ten} đồng ý.",
                      "Người cùng đứng tên bán là {ben_ban_vc_quan_he} tôi, {ben_ban_vc_ho_ten}."],
    "seller_spouse_list": ["và {ben_ban_vc_quan_he}: {ben_ban_vc_ho_ten}"],
    "narrative_buyer": ["Nay tôi đồng ý sang lại cho {ben_mua_goi} {ben_mua_ho_ten}, sinh năm {ben_mua_nam_sinh}, ngụ tại {ben_mua_dia_chi},",
                        "Nay tôi làm giấy này bán cho {ben_mua_goi} {ben_mua_ho_ten}, sinh năm {ben_mua_nam_sinh}, ở tại {ben_mua_dia_chi},"],
    "land": ["một miếng đất thổ cư diện tích {dien_tich} (ngang {rong}, dài {dai}), tọa lạc tại {dia_chi_dat}.",
             "một lô đất có diện tích {dien_tich}, chiều ngang {rong}, chiều dài {dai}, tại {dia_chi_dat}.",
             "Bên A đồng ý sang cho bên B một miếng đất diện tích {dien_tich} (ngang {rong} x dài {dai}) tại {dia_chi_dat}."],
    "bounds": ["Đông giáp {tu_can_dong}; Tây giáp {tu_can_tay}; Nam giáp {tu_can_nam}; Bắc giáp {tu_can_bac}.",
               "Tứ cận: Đông giáp {tu_can_dong}, Tây giáp {tu_can_tay}, Nam giáp {tu_can_nam}, Bắc giáp {tu_can_bac}."],
    "price": ["Giá sang là {gia} (bằng chữ: {gia_bang_chu}).",
              "Với số tiền là {gia} ({gia_bang_chu}). Bên B đã giao đủ, bên A đã nhận đủ.",
              "Giá hai bên thỏa thuận: {gia}. Bằng chữ: {gia_bang_chu}."],
    "commit": ["Kể từ ngày ký giấy này, miếng đất trên thuộc quyền sử dụng của bên mua.",
               "Bên bán cam kết đất không có tranh chấp, nếu có tranh chấp bên bán hoàn toàn chịu trách nhiệm.",
               "Giấy này làm thành 02 bản, mỗi bên giữ 01 bản có giá trị như nhau.",
               "Hai bên cam kết thực hiện đúng, không ai được thay đổi ý kiến."],
    "sign_seller": ["Bên sang", "Người bán", "Bên A"],
    "sign_buyer": ["Bên nhận sang", "Người mua", "Bên B"],
    "sign_witness": ["Người làm chứng", "Người chứng kiến"],
}


def parse(text: str, fields: dict) -> list[dict] | None:
    """Chuỗi có chỗ trống -> segments. None nếu có trường bỏ trống hoặc không tồn tại."""
    segments, pos = [], 0
    for m in PLACEHOLDER.finditer(text):
        name = m.group(1)
        if name not in fields or not fields[name]["text"]:
            return None
        if m.start() > pos:
            segments.append({"t": text[pos:m.start()]})
        segments.append({"f": name})
        pos = m.end()
    if pos < len(text):
        segments.append({"t": text[pos:]})
    return segments


def _join(parts: list[str], fields: dict) -> list[dict]:
    """Ghép các mệnh đề bằng dấu phẩy, bỏ mệnh đề có trường trống."""
    kept = [s for s in (parse(p, fields) for p in parts) if s]
    out = []
    for i, s in enumerate(kept):
        if i:
            out.append({"t": ", "})
        out += s
    return out


def _party(rng: random.Random, fields: dict, role: str) -> list[dict]:
    """Một bên theo kiểu liệt kê: tên, năm sinh, CMND (nếu có), địa chỉ."""
    head = rng.choice(PHRASES[f"{'seller' if role == 'ben_ban' else 'buyer'}_list"])
    parts = list(head)
    parts.append(rng.choice(PHRASES["id"]).replace("{cmnd}", f"{{{role}_cmnd}}"))
    if role == "ben_ban":
        parts.append(PHRASES["seller_spouse_list"][0])
    lines = [{"kind": "para", "align": "left", "segments": _join(parts, fields)}]
    addr = parse(rng.choice(PHRASES["addr"]).replace("{dia_chi}", f"{{{role}_dia_chi}}"), fields)
    if addr:
        lines.append({"kind": "para", "align": "left", "indent": True, "segments": addr})
    return lines


def giay_sang_dat(rng: random.Random, fields: dict) -> list[dict]:
    def block(kind, text, align="left"):
        segs = parse(text, fields)
        return {"kind": kind, "align": align, "segments": segs} if segs else None

    blocks = []
    if rng.random() < 0.5:
        blocks.append({"kind": "quoc_hieu", "align": "center", "segments": []})
    date_on_top = rng.random() < 0.5
    if date_on_top:
        blocks.append(block("para", rng.choice(PHRASES["place_date"]), "right"))
    blocks.append(block("title", rng.choice(PHRASES["title"]), "center"))

    if rng.random() < 0.5:
        blocks.append(block("para", rng.choice(PHRASES["intro"]) if not date_on_top else "Chúng tôi gồm có:"))
        blocks += _party(rng, fields, "ben_ban")
        blocks += _party(rng, fields, "ben_mua")
        blocks.append(block("para", rng.choice(PHRASES["land"][2:])))
    else:
        blocks.append(block("para", rng.choice(PHRASES["narrative_seller"])))
        blocks.append(block("para", rng.choice(PHRASES["seller_spouse"])))
        blocks.append(block("para", rng.choice(PHRASES["narrative_buyer"]) + " " + rng.choice(PHRASES["land"][:2])))
    blocks.append(block("para", rng.choice(PHRASES["bounds"])))
    blocks.append(block("para", rng.choice(PHRASES["price"])))
    for text in rng.sample(PHRASES["commit"], rng.randint(1, 3)):
        blocks.append(block("para", text))
    if not date_on_top:
        blocks.append(block("para", rng.choice(PHRASES["place_date"]), "right"))

    signers = [(rng.choice(PHRASES["sign_seller"]), "ben_ban_ho_ten"), (rng.choice(PHRASES["sign_buyer"]), "ben_mua_ho_ten")]
    if fields.get("ben_ban_vc_ho_ten", {}).get("text"):
        signers.insert(1, (fields["ben_ban_vc_quan_he"]["text"].capitalize() + " bên bán", "ben_ban_vc_ho_ten"))
    if fields.get("lam_chung_ho_ten", {}).get("text"):
        signers.append((rng.choice(PHRASES["sign_witness"]), "lam_chung_ho_ten"))
    if rng.random() < 0.5:
        signers[0], signers[1] = signers[1], signers[0]
    blocks.append({"kind": "signatures", "align": "center",
                   "signers": [{"label": label, "field": name} for label, name in signers], "segments": []})
    return [b for b in blocks if b]


BUILDERS = {"giay_sang_dat": giay_sang_dat}


def used_fields(blocks: list[dict]) -> set[str]:
    used = {s["f"] for b in blocks for s in b["segments"] if "f" in s}
    return used | {s["field"] for b in blocks for s in b.get("signers", [])}


def build(kind: str, rng: random.Random, fields: dict) -> list[dict]:
    return BUILDERS[kind](rng, fields)
