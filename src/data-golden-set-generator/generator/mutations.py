"""Gây lỗi có chủ đích trên hồ sơ hợp lệ. Mỗi hàm trả về mô tả lý do để ghi vào ground truth.

`persona_override` không nằm ở đây: nó áp dụng lúc dựng persona (dossier.build).
"""

import random
from datetime import timedelta

from generator.fields import address, dates
from generator.values import dossier_ctx, for_variant, format_text, resolve_path


def _find_doc(dossier: dict, doc_type: str) -> dict:
    return next(d for d in dossier["documents"] if d["doc_type"] == doc_type)


def _set_field(doc: dict, schema, name: str, value, mutation_id: str) -> dict:
    f = doc["fields"][name]
    old = f["text"]
    f["value"] = value
    f["text"] = format_text(for_variant(schema.field_spec(name), doc.get("variant")), value)
    f["mutated_by"] = mutation_id
    return {"old": old, "new": f["text"]}


def _perturb(rng: random.Random, kind: str, value):
    match kind:
        case "date_shift":
            delta = rng.choice([1, -1]) * rng.choice([1, 2, 10, 31, 365])
            return value + timedelta(days=delta)
        case "swap_digits":
            s = list(value)
            pairs = [i for i in range(len(s) - 1) if s[i] != s[i + 1]]
            if not pairs:  # "7", "11": không đảo được thì đổi một chữ số
                i = rng.randrange(len(s))
                s[i] = rng.choice([c for c in "0123456789" if c != s[i]])
                return "".join(s)
            i = rng.choice(pairs)
            s[i], s[i + 1] = s[i + 1], s[i]
            return "".join(s)
        case "typo_name":
            words = value.split()
            i = rng.randrange(len(words))
            w = words[i]
            j = rng.randrange(len(w))
            words[i] = w[:j] + w[j + 1:] if len(w) > 2 else w + w[-1]
            return " ".join(words)
        case "area_shift":
            # Diện tích lệch 1-8%: đo đạc lại khác giấy chứng nhận, hoặc ghi sai.
            return round(value * (1 + rng.choice([1, -1]) * rng.uniform(0.01, 0.08)), 1)
        case "year_shift":
            return dates.add_years(value, rng.choice([1, -1]) * rng.randint(1, 3))
        case "other_address":
            new = value
            while new == value:
                new = address.format(address.generate(rng))
            return new
    raise ValueError(f"perturb không hỗ trợ: {kind}")


def missing_document(rng, dossier, proc, m):
    doc_type = m["params"]["doc_type"]
    dossier["documents"] = [d for d in dossier["documents"] if d["doc_type"] != doc_type]
    dossier["missing_documents"].append(doc_type)
    return f"Thiếu giấy tờ {proc.schemas[doc_type].title}"


def field_conflict(rng, dossier, proc, m):
    p = m["params"]
    doc = _find_doc(dossier, p["doc_type"])
    value = doc["fields"][p["field"]]["value"]
    change = _set_field(doc, proc.schemas[p["doc_type"]], p["field"], _perturb(rng, p["perturb"], value), m["id"])
    return f"{proc.schemas[p['doc_type']].title}: {p['field']} ghi '{change['new']}', các giấy tờ khác ghi '{change['old']}'"


def field_value(rng, dossier, proc, m):
    """Đặt một trường thành giá trị cố định vi phạm quy tắc, ví dụ mục đích không thuộc phạm vi thủ tục."""
    p = m["params"]
    doc = _find_doc(dossier, p["doc_type"])
    value = rng.choice(p["values"])
    change = _set_field(doc, proc.schemas[p["doc_type"]], p["field"], value, m["id"])
    return f"{proc.schemas[p['doc_type']].title}: {p['field']} = '{change['new']}'"


def date_order(rng, dossier, proc, m):
    p = m["params"]
    doc = _find_doc(dossier, p["doc_type"])
    anchor = dates.parse(resolve_path(p["after"], dossier_ctx(dossier)))
    value = anchor + timedelta(days=rng.randint(1, 30))
    change = _set_field(doc, proc.schemas[p["doc_type"]], p["field"], value, m["id"])
    return f"{proc.schemas[p['doc_type']].title}: {p['field']} ({change['new']}) sau {p['after']}"


MUTATORS = {
    "missing_document": missing_document,
    "field_conflict": field_conflict,
    "field_value": field_value,
    "date_order": date_order,
}


def apply(rng: random.Random, dossier: dict, proc, m: dict) -> dict:
    detail = MUTATORS[m["kind"]](rng, dossier, proc, m)
    return {"rule": m["expect"]["rule"], "mutation": m["id"], "detail": detail}
