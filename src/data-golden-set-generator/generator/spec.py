"""Đọc procedure.yaml và schema.yaml (định dạng: specs/*.example.yaml)."""

import re
from dataclasses import dataclass, field

import yaml

from generator import TEMPLATES_DIR


@dataclass
class DocSchema:
    doc_type: str
    version: int
    title: str
    fields: list[dict]
    issue_date: dict = field(default_factory=lambda: {"offset_days": [-30, 0]})
    decorations: list[dict] = field(default_factory=list)
    variants: dict = field(default_factory=dict)
    render: dict = field(default_factory=dict)
    groups: list[dict] = field(default_factory=list)
    freeform: str | None = None
    procedure: str = ""            # Thư mục thủ tục chứa schema và template (khác thủ tục đang sinh khi dùng `from`)
    raw: dict = field(default_factory=dict)

    @property
    def template(self) -> str:
        return f"{self.procedure}/{self.doc_type}/template.html.j2"

    def field_spec(self, name: str) -> dict:
        """Tìm cả trường của nhóm lặp: 'tv2_ho_ten' -> spec 'ho_ten' của nhóm 'tv'."""
        for f in self.fields:
            if f["name"] == name:
                return f
        for g in self.groups:
            m = re.fullmatch(rf"{g['name']}\d+_(\w+)", name)
            if m:
                return {**next(f for f in g["fields"] if f["name"] == m.group(1)), "name": name}
        raise KeyError(name)


@dataclass
class Procedure:
    name: str
    title: str
    documents: list[dict]
    rules: dict[str, str]
    mutations: list[dict]
    mix: dict[str, float]
    persona: dict
    submit_date: list[str]
    schemas: dict[str, DocSchema]
    people: str | None = None
    coverage: list[dict] = field(default_factory=list)
    province: str | None = None    # Nhà đất và người nộp chỉ thuộc tỉnh/thành phố này
    thu_hoi: str | None = None     # Bộ quy định tính bồi thường (generator/thu_hoi.py), ví dụ tphcm-2026


def list_procedures() -> list[str]:
    return sorted(p.parent.name for p in TEMPLATES_DIR.glob("*/procedure.yaml"))


def load_schema(procedure: str, doc_type: str) -> DocSchema:
    raw = yaml.safe_load((TEMPLATES_DIR / procedure / doc_type / "schema.yaml").read_text(encoding="utf-8"))
    return DocSchema(
        doc_type=raw["doc_type"],
        version=raw.get("version", 1),
        title=raw["title"],
        fields=raw["fields"],
        issue_date=raw.get("issue_date", {"offset_days": [-30, 0]}),
        decorations=raw.get("decorations", []),
        variants=raw.get("variants", {}),
        render=raw.get("render", {}),
        groups=raw.get("groups", []),
        freeform=raw.get("freeform"),
        procedure=procedure,
        raw=raw,
    )


def load_procedure(name: str) -> Procedure:
    raw = yaml.safe_load((TEMPLATES_DIR / name / "procedure.yaml").read_text(encoding="utf-8"))
    rule_ids = {r["id"]: r["text"] for r in raw.get("rules", [])}
    for m in raw.get("mutations", []):
        rule = m["expect"]["rule"]
        if rule not in rule_ids:
            raise ValueError(f"{name}: mutation {m['id']} tham chiếu quy tắc không tồn tại {rule}")
    known = {d["doc_type"] for d in raw["documents"]}
    for dim in raw.get("coverage", []):
        for value, expect in dim["values"].items():
            if set(expect) - known:
                raise ValueError(f"{name}: coverage {dim['name']}={value} tham chiếu giấy tờ không có: {set(expect) - known}")
    return Procedure(
        name=raw["procedure"],
        title=raw["title"],
        documents=raw["documents"],
        rules=rule_ids,
        mutations=raw.get("mutations", []),
        mix=raw.get("mix", {"valid": 1.0, "invalid": 0.0}),
        persona=raw.get("persona", {}),
        submit_date=raw["submit_date"],
        # `from`: dùng lại schema và template của thủ tục khác, ví dụ 7 giấy tờ của giai-toa-den-bu.
        schemas={d["doc_type"]: load_schema(d.get("from", name), d["doc_type"]) for d in raw["documents"]},
        people=raw.get("people"),
        coverage=raw.get("coverage", []),
        province=raw.get("province"),
        thu_hoi=raw.get("thu_hoi"),
    )
