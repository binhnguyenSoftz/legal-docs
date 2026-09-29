"""Dựng một hồ sơ: persona (+ nhóm người, thửa đất nếu thủ tục cần) + các giấy tờ + (tùy chọn) một lỗi có chủ đích + nhãn quyết định."""

import random
from datetime import timedelta

from generator import GENERATOR_VERSION, freeform, mutations, people, persona, property, style
from generator.fields import dates
from generator.rng import derive_seed, weighted_choice
from generator.spec import DocSchema, Procedure
from generator.values import compute_value, dossier_ctx, make_field, resolve_path

PERSONA_OVERRIDE = "persona_override"
# Số lần sinh lại tối đa để khớp kịch bản biến thể. Hết lượt thì lấy lần khớp nhiều chiều nhất.
MAX_ATTEMPTS = 40


def plan(proc: Procedure, index: int) -> dict[str, str]:
    """Kịch bản biến thể của hồ sơ thứ index: {tên chiều: giá trị} theo mục coverage của procedure.

    Chữ số cơ số hỗn hợp của index, cộng dồn: mọi chiều đổi giá trị ở mỗi hồ sơ (cân bằng với mọi số lượng),
    và cứ đủ tích số giá trị các chiều thì phủ hết mọi tổ hợp.
    """
    digits, m = [], 1
    for dim in proc.coverage:
        n = len(dim["values"])
        digits.append(index // m % n)
        m *= n
    return {dim["name"]: list(dim["values"])[(digits[k] + sum(digits[:k])) % len(dim["values"])]
            for k, dim in enumerate(proc.coverage)}


def expected_variants(proc: Procedure, targets: dict[str, str]) -> dict[str, str]:
    """Kịch bản -> biến thể kỳ vọng của từng giấy tờ."""
    out = {}
    for dim in proc.coverage:
        if dim["name"] in targets:
            out.update(dim["values"][targets[dim["name"]]])
    return out


def _pick_mutation(rng: random.Random, proc: Procedure) -> dict | None:
    if not proc.mutations or rng.random() >= proc.mix.get("invalid", 0):
        return None
    return weighted_choice(rng, proc.mutations, [m.get("weight", 1) for m in proc.mutations])


def _pick_variant(rng: random.Random, spec: dict, ctx: dict, forced: str | None = None) -> str | None:
    """Biến thể mẫu của giấy tờ. Có `by`: chọn case đầu tiên khớp điều kiện; không có: chọn ngẫu nhiên theo weight
    (hoặc theo kịch bản nếu có `forced`)."""
    cases = spec.get("cases", [])
    if not cases:
        return None
    if "by" not in spec:
        if forced in {c["name"] for c in cases}:
            return forced
        return weighted_choice(rng, cases, [c.get("weight", 1) for c in cases])["name"]
    value = resolve_path(spec["by"], ctx)
    for c in cases:
        if "before" in c and not value < dates.parse(c["before"]):
            continue
        if "equals" in c and value != c["equals"]:
            continue
        return c["name"]
    raise ValueError(f"Không có biến thể khớp {spec['by']} = {value}")


def _issue_date(rng: random.Random, schema: DocSchema, ctx: dict):
    spec = schema.issue_date
    base = dates.parse(resolve_path(spec["source"], ctx)) if "source" in spec else ctx["dossier"]["submit_date"]
    lo, hi = spec.get("offset_days", [-30, 0] if "source" not in spec else [0, 0])
    return base + timedelta(days=rng.randint(lo, hi))


def _build_document(rng: random.Random, proc: Procedure, doc_type: str, index: int, ctx: dict,
                    forced_variant: str | None = None) -> dict:
    schema = proc.schemas[doc_type]
    issue = _issue_date(rng, schema, ctx)
    doc_ctx = {**ctx, "doc": {"issue_date": issue}}
    variant = _pick_variant(rng, schema.variants, doc_ctx, forced_variant)
    doc_ctx["doc"]["variant"] = variant

    fields = {}
    for spec in schema.fields:
        if "variants" in spec and variant not in spec["variants"]:
            continue
        fields[spec["name"]] = make_field(spec, compute_value(spec, rng, doc_ctx), variant)
    for spec in schema.fields:
        # blank_if: trường đi kèm (ví dụ ngày của một dòng biến động) trống theo trường chính.
        if spec["name"] in fields and "blank_if" in spec and fields[spec["blank_if"]]["value"] is None:
            fields[spec["name"]] = make_field(spec, None, variant)
    groups = {}
    for g in schema.groups:
        items = resolve_path(g["items"], doc_ctx)[: g.get("max")]
        groups[g["name"]] = len(items)
        for i, item in enumerate(items, start=1):
            item_ctx = {**doc_ctx, "item": item}
            for spec in g["fields"]:
                spec = {**spec, "name": f"{g['name']}{i}_{spec['name']}"}
                fields[spec["name"]] = make_field(spec, compute_value(spec, rng, item_ctx), variant)

    doc = {
        "doc_id": f"{index:02d}-{doc_type}",
        "doc_type": doc_type,
        "schema_version": schema.version,
        "title": schema.title,
        "issue_date": issue,
        "variant": variant,
        "render": style.doc_style(rng, schema.render),
        "groups": groups,
        "fields": fields,
        "files": {},
    }
    if schema.freeform:
        doc["blocks"] = freeform.build(schema.freeform, rng, fields)
        # Bố cục tự do không dùng hết các trường: trường không có trên giấy thì không có trong ground truth.
        used = freeform.used_fields(doc["blocks"])
        doc["fields"] = {n: f for n, f in fields.items() if n in used}
    return doc


def _knobs(proc: Procedure, targets: dict[str, str]) -> dict:
    """Kịch bản -> tham số điều hướng generator: thế hệ thẻ, thời kỳ người mất."""
    knobs = {}
    for dim in proc.coverage:
        if dim["name"] in targets and dim.get("knob") in ("persona.card", "people.nam_mat", "people.nguon_goc"):
            knobs[dim["knob"]] = targets[dim["name"]]
    return knobs


def _build_once(proc: Procedure, master_seed: int, index: int, attempt: int, targets: dict[str, str]) -> dict:
    parts = (proc.name, index) if attempt == 0 else (proc.name, index, attempt)
    seed = derive_seed(master_seed, *parts)
    rng = random.Random(seed)
    knobs = _knobs(proc, targets)
    forced = expected_variants(proc, targets)

    # Ca lỗi chọn bằng rng riêng, không đổi qua các lần sinh lại: sinh lại chỉ để khớp kịch bản biến thể.
    mutation = _pick_mutation(random.Random(derive_seed(master_seed, proc.name, index, "mutation")), proc)
    submit_date = dates.between(rng, dates.parse(proc.submit_date[0]), dates.parse(proc.submit_date[1]))

    persona_params = {"age": tuple(proc.persona.get("age", (18, 70))), "gender": proc.persona.get("gender", "any"),
                      "card": knobs.get("persona.card")}
    if mutation and mutation["kind"] == PERSONA_OVERRIDE:
        persona_params.update({k: tuple(v) if isinstance(v, list) else v for k, v in mutation["params"].items()})
    person = persona.build(rng, submit_date, **persona_params)

    dossier = {
        "dossier_id": f"{proc.name}-{master_seed}-{index:05d}",
        "procedure": proc.name,
        "procedure_title": proc.title,
        "seed": seed,
        "generator_version": GENERATOR_VERSION,
        "submit_date": submit_date,
        "persona": person,
        "documents": [],
        "missing_documents": [],
    }
    if proc.people == "deceased_owner":
        fam = people.build(rng, submit_date, person, knobs.get("people.nam_mat"), knobs.get("people.nguon_goc"))
        dossier.update(fam)
        dossier["property"] = property.build(rng, person["noi_thuong_tru_parts"], fam["timeline"]["ngay_sang"],
                                             fam["timeline"]["ngay_cap_gcn"])
        dossier["compensation"] = people.compensation(fam, dossier["property"], submit_date)
    elif proc.people:
        raise ValueError(f"{proc.name}: people không hỗ trợ: {proc.people}")

    ctx = {**dossier_ctx(dossier), "procedure_title": proc.title}
    for i, d in enumerate(proc.documents, start=1):
        dossier["documents"].append(_build_document(rng, proc, d["doc_type"], i, ctx, forced.get(d["doc_type"])))

    reasons = []
    if mutation:
        if mutation["kind"] == PERSONA_OVERRIDE:
            reasons.append({"rule": mutation["expect"]["rule"], "mutation": mutation["id"],
                            "detail": f"Persona sinh ngoài điều kiện: {mutation['params']}"})
        else:
            reasons.append(mutations.apply(rng, dossier, proc, mutation))

    dossier["decision"] = {
        "label": mutation["expect"]["decision"] if mutation else "approve",
        "reasons": reasons,
    }
    dossier["review"] = {"status": "unreviewed", "reviewer": None, "note": None}
    return dossier


def _mismatches(proc: Procedure, d: dict, targets: dict[str, str]) -> list[str]:
    """Các chiều của kịch bản chưa đạt. Ca lỗi ép thẻ (CMND) được miễn chiều thẻ: ca lỗi ưu tiên hơn kịch bản."""
    variants = {doc["doc_type"]: doc["variant"] for doc in d["documents"]}
    forced_card = bool(d["persona"]["the"]) and d["persona"]["the"]["loai"] == "cmnd-9"
    bad = []
    for dim in proc.coverage:
        if dim["name"] not in targets:
            continue
        if forced_card and dim.get("knob") == "persona.card":
            continue
        expect = dim["values"][targets[dim["name"]]]
        if any(variants.get(t) != v for t, v in expect.items()):
            bad.append(dim["name"])
        elif dim.get("knob") == "people.nguon_goc" and people.land_era(d["timeline"]["ngay_sang"]) != targets[dim["name"]]:
            bad.append(dim["name"])
    return bad


def build(proc: Procedure, master_seed: int, index: int, coverage: bool = True) -> dict:
    """Dựng hồ sơ thứ index. coverage=True: theo kịch bản biến thể của procedure, sinh lại tới khi khớp."""
    targets = plan(proc, index) if coverage and proc.coverage else {}
    best, tries = None, 0
    for attempt in range(MAX_ATTEMPTS if targets else 1):
        tries += 1
        d = _build_once(proc, master_seed, index, attempt, targets)
        bad = _mismatches(proc, d, targets)
        if best is None or len(bad) < len(best[1]):
            best = (d, bad)
        if not bad:
            break
    d, bad = best
    d["profile"] = {
        "targets": targets,
        "variants": {doc["doc_type"]: doc["variant"] for doc in d["documents"]},
        "unmet": bad,
        "attempts": tries,
    }
    return d
