"""Tính giá trị và chuỗi hiển thị của một trường theo schema."""

import random
import re
from datetime import date, timedelta

from generator.fields import address, cccd, dates, money, names, phone
from generator.text import llm_text


def resolve_path(path: str, ctx: dict):
    """'persona.ho_ten' -> ctx['persona']['ho_ten']. Phần tử danh sách: 'people.con.0.ho_ten'. Thuộc tính: 'timeline.ngay_sang.year'."""
    obj = ctx
    for part in path.split("."):
        if isinstance(obj, (list, tuple)):
            obj = obj[int(part)]
        elif isinstance(obj, dict):
            obj = obj[part]
        else:
            obj = getattr(obj, part)
    return obj


def dossier_ctx(dossier: dict) -> dict:
    """Ngữ cảnh để schema và mutation tham chiếu: persona, people, timeline, property, dossier."""
    return {"dossier": dossier, "persona": dossier["persona"], "people": dossier.get("people"),
            "timeline": dossier.get("timeline"), "property": dossier.get("property")}


def _date_param(value, ctx) -> date:
    return dates.parse(resolve_path(value, ctx) if isinstance(value, str) and "." in value else value)


def _gen_choice(rng, params, ctx):
    return rng.choices(params["values"], weights=params.get("weights"), k=1)[0]


def _gen_date_between(rng, params, ctx):
    return dates.between(rng, _date_param(params["start"], ctx), _date_param(params["end"], ctx))


def _gen_date_offset(rng, params, ctx):
    """Ngày lệch [lo, hi] ngày so với một ngày trong ctx."""
    lo, hi = params["days"]
    return _date_param(params["source"], ctx) + timedelta(days=rng.randint(lo, hi))


def _gen_address_at(rng, params, ctx):
    """Địa chỉ ghi theo thời kỳ của giấy tờ: 3 cấp trước 01/7/2025, 2 cấp từ mốc này."""
    parts = resolve_path(params["source"], ctx)
    at = _date_param(params.get("at", "doc.issue_date"), ctx)
    return address.place(parts, at) if params.get("kind") == "place" else address.format_at(parts, at)


OCCUPATIONS = {
    "child": ["Học sinh"],
    "young": ["Sinh viên", "Công nhân", "Lao động tự do", "Buôn bán", "Bộ đội"],
    "adult": ["Buôn bán", "Công nhân", "Cán bộ", "Nội trợ", "Lao động tự do", "Làm ruộng", "Giáo viên", "Bộ đội",
              "Thợ may", "Thợ mộc", "Tài xế", "Kế toán", "Y tá", "Công nhân viên chức"],
    "old": ["Hưu trí", "Nội trợ", "Làm ruộng", "Buôn bán"],
}


def _gen_occupation(rng, params, ctx):
    """Nghề nghiệp hợp với tuổi của người đó tại ngày lập giấy tờ. Chưa đi học hoặc chưa sinh: None."""
    person = resolve_path(params.get("person", "item"), ctx)
    age = dates.age_on(person["ngay_sinh"], _date_param(params.get("at", "doc.issue_date"), ctx))
    if age < 6:
        return None
    group = "child" if age < 18 else "young" if age < 23 else "adult" if age < 60 else "old"
    return rng.choice(OCCUPATIONS[group])


def _gen_pattern(rng, params, ctx):
    """'#' -> một chữ số. Ví dụ '###/2001/QSDĐ'."""
    return "".join(str(rng.randrange(10)) if c == "#" else c for c in params["pattern"])


def _gen_template(rng, params, ctx):
    """Ghép chuỗi từ đường dẫn trong ctx: 'Thửa {property.so_thua}'."""
    return re.sub(r"\{([\w.]+)\}", lambda m: str(resolve_path(m.group(1), ctx)), params["text"])


GENERATORS = {
    "choice": _gen_choice,
    "const": lambda rng, params, ctx: params["value"],
    "date_between": _gen_date_between,
    "date_offset": _gen_date_offset,
    "address_at": _gen_address_at,
    "pattern": _gen_pattern,
    "occupation": _gen_occupation,
    "template": _gen_template,
    "phone": lambda rng, params, ctx: phone.generate(rng),
    "person_name": lambda rng, params, ctx: names.generate(rng, params.get("gender") or rng.choice(["male", "female"]))["ho_ten"],
    "cccd": lambda rng, params, ctx: cccd.generate(rng, ctx["persona"]["ngay_sinh"], ctx["persona"]["gender"]),
    "llm_text": llm_text,
}


def compute_value(spec: dict, rng: random.Random, ctx: dict):
    if spec.get("blank_rate") and rng.random() < spec["blank_rate"]:
        return None
    if "source" in spec:
        return resolve_path(spec["source"], ctx)
    return GENERATORS[spec["gen"]](rng, spec.get("params", {}), ctx)


def format_text(spec: dict, value) -> str:
    """Chuỗi đúng như in trên giấy: đây là nhãn cho tầng OCR."""
    if value is None:
        return spec.get("null_text", "")
    if isinstance(value, bool):
        return ""
    fmt = spec.get("format")
    if isinstance(value, date):
        text = value.strftime(fmt or "%d/%m/%Y")
    elif isinstance(value, (int, float)) and fmt == "vn_decimal":
        text = money.decimal(value, spec.get("digits", 1))
    elif isinstance(value, int) and fmt == "vn_group":
        text = money.group(value)
    elif isinstance(value, int) and fmt == "vn_words":
        text = money.to_words(value)
    else:
        text = str(value)
    match spec.get("transform"):
        case "upper":
            text = text.upper()
        case "lower":
            text = text.lower()
        case "title":
            text = text.title()
    return spec.get("prefix", "") + text + spec.get("suffix", "")


def for_variant(spec: dict, variant: str | None) -> dict:
    """Ghi đè spec theo biến thể mẫu: `by_variant: {<tên biến thể>: {fill: ..., format: ...}}`."""
    return {**spec, **spec.get("by_variant", {}).get(variant, {})}


def make_field(spec: dict, value, variant: str | None = None) -> dict:
    spec = for_variant(spec, variant)
    return {
        "name": spec["name"],
        "type": spec["type"],
        "value": value,
        "text": format_text(spec, value),
        "fill": spec.get("fill", "handwritten"),
        "mutated_by": None,
        "bbox": [],
    }
