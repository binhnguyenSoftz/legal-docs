import argparse
import csv
import json
import random
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from generator import GENERATED_DIR, GENERATOR_VERSION, dossier, spec
from generator.rng import derive_seed


def _json_default(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(type(obj))


def to_ground_truth(d: dict) -> dict:
    """Chuyển bản ghi hồ sơ nội bộ sang định dạng specs/ground_truth.schema.json."""
    gt = {
        "dossier_id": d["dossier_id"],
        "procedure": d["procedure"],
        "seed": d["seed"],
        "generator_version": d["generator_version"],
        "submit_date": d["submit_date"],
        "persona": d["persona"],
    }
    for key in ("people", "timeline", "property", "compensation"):
        if key in d:
            gt[key] = d[key]
    return gt | {
        "documents": [
            {
                "doc_id": doc["doc_id"],
                "doc_type": doc["doc_type"],
                "schema_version": doc["schema_version"],
                "variant": doc.get("variant"),
                "issue_date": doc["issue_date"],
                "render": {k: v for k, v in doc["render"].items() if k not in ("stains", "hw_font")},
                "fields": list(doc["fields"].values()),
                "files": doc["files"],
            }
            for doc in d["documents"]
        ],
        "missing_documents": d["missing_documents"],
        "profile": d.get("profile"),
        "decision": d["decision"],
        "review": d["review"],
    }


def index_row(d: dict) -> dict:
    """Một dòng index.csv: đủ để lọc kết quả đánh giá theo nhãn, ca lỗi, biến thể mà không cần mở ground truth."""
    reasons = d["decision"]["reasons"]
    profile = d.get("profile") or {}
    row = {
        "dossier_id": d["dossier_id"],
        "seed": d["seed"],
        "submit_date": d["submit_date"].isoformat(),
        "label": d["decision"]["label"],
        "mutation": ";".join(r["mutation"] for r in reasons),
        "rule": ";".join(r["rule"] for r in reasons),
        "documents": len(d["documents"]),
        "pages": sum(len(doc["files"].get("pages", [])) for doc in d["documents"]),
        "unmet": ";".join(profile.get("unmet", [])),
    }
    if "compensation" in d:
        c = d["compensation"]
        row |= {"nguon_goc_dat": c["nguon_goc_dat"], "dien_tich_dat": c["dien_tich_dat"],
                "nhan_khau": c["nhan_khau"], "nguoi_thua_ke": len(c["nguoi_thua_ke"])}
    row |= {f"target:{k}": v for k, v in profile.get("targets", {}).items()}
    row |= {f"variant:{doc['doc_type']}": doc["variant"] or "" for doc in d["documents"]}
    return row


def cmd_list(args):
    for name in spec.list_procedures():
        proc = spec.load_procedure(name)
        print(f"{name}\t{proc.title}\t{', '.join(proc.schemas)}")


def cmd_generate(args):
    proc = spec.load_procedure(args.procedure)
    levels = [lv for lv in args.noise.split(",") if lv]
    out_root = Path(args.out) / str(args.seed)
    out_root.mkdir(parents=True, exist_ok=True)

    renderer = None
    if not args.no_render:
        from generator.render import Renderer
        renderer = Renderer(dpi=args.dpi)
    if levels:
        from generator import noise

    labels = {}
    rows = []
    try:
        for i in range(args.count):
            d = dossier.build(proc, args.seed, i, coverage=args.coverage == "balanced")
            out_dir = out_root / d["dossier_id"]
            out_dir.mkdir(exist_ok=True)
            if renderer:
                from generator.render import pick_style
                style = pick_style(random.Random(derive_seed(d["seed"], "style")))
                for doc in d["documents"]:
                    renderer.render(proc.name, doc, d, style, out_dir)
                    for page_no, png in enumerate(doc["files"]["pages"], start=1):
                        page_boxes = {n: [b for b in f["bbox"] if b["page"] == page_no] for n, f in doc["fields"].items()}
                        page_boxes = {n: bs for n, bs in page_boxes.items() if bs}
                        for level in levels:
                            rec = noise.apply(out_dir / png, page_boxes, level,
                                              derive_seed(d["seed"], doc["doc_id"], page_no, level),
                                              out_dir / f"{Path(png).stem}_{level}.jpg")
                            doc["files"]["noisy"].append({"page": page_no, **rec})
            gt = to_ground_truth(d)
            (out_dir / "ground_truth.json").write_text(
                json.dumps(gt, ensure_ascii=False, indent=2, default=_json_default), encoding="utf-8")
            labels[d["decision"]["label"]] = labels.get(d["decision"]["label"], 0) + 1
            rows.append(index_row(d))
    finally:
        if renderer:
            renderer.close()

    columns = list(dict.fromkeys(k for r in rows for k in r))
    with open(out_root / f"index-{proc.name}.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    variants = {}
    for r in rows:
        for k, v in r.items():
            if k.startswith("variant:"):
                variants.setdefault(k[len("variant:"):], {}).setdefault(v, 0)
                variants[k[len("variant:"):]][v] += 1

    manifest = {
        "procedure": proc.name,
        "seed": args.seed,
        "count": args.count,
        "noise": levels,
        "dpi": args.dpi,
        "generator_version": GENERATOR_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "coverage": args.coverage,
        "labels": labels,
        "variants": variants,
        "unmet": sum(1 for r in rows if r["unmet"]),
    }
    (out_root / f"manifest-{proc.name}.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


def cmd_inspect(args):
    """Vẽ bbox lên ảnh sạch và ảnh nhiễu để kiểm tra bằng mắt: <tên>_bbox.jpg."""
    import cv2

    folder = Path(args.dossier_dir)
    gt = json.loads((folder / "ground_truth.json").read_text(encoding="utf-8"))
    for doc in gt["documents"]:
        targets = [(p, i, {f["name"]: [b for b in f["bbox"] if b["page"] == i] for f in doc["fields"]})
                   for i, p in enumerate(doc["files"].get("pages", []), start=1)]
        targets += [(n["path"], n["page"], n["bboxes"]) for n in doc["files"].get("noisy", [])]
        for path, _, boxes in targets:
            img = cv2.imread(str(folder / path))
            for name, bs in boxes.items():
                for b in bs:
                    p0 = (int(b["x"]), int(b["y"]))
                    p1 = (int(b["x"] + b["w"]), int(b["y"] + b["h"]))
                    cv2.rectangle(img, p0, p1, (0, 0, 255), 2)
                    cv2.putText(img, name, (p0[0], p0[1] - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            out = folder / f"{Path(path).stem}_bbox.jpg"
            cv2.imwrite(str(out), img)
            print(out)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="generator", description=f"Golden set generator v{GENERATOR_VERSION}")
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("list", help="Liệt kê thủ tục đã có template")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("generate", help="Sinh hồ sơ")
    p.add_argument("--procedure", required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--count", type=int, default=10)
    p.add_argument("--noise", default="light,medium,heavy", help="Các mức nhiễu, phân cách dấu phẩy. Rỗng = chỉ bản sạch")
    p.add_argument("--dpi", type=int, default=200)
    p.add_argument("--no-render", action="store_true", help="Chỉ sinh ground_truth.json, bỏ qua render và nhiễu")
    p.add_argument("--out", default=str(GENERATED_DIR))
    p.add_argument("--coverage", choices=["balanced", "random"], default="balanced",
                   help="balanced: mỗi hồ sơ theo một kịch bản biến thể, xoay vòng cho đều (mục coverage của procedure). "
                        "random: biến thể theo phân bố tự nhiên")
    p.set_defaults(func=cmd_generate)

    p = sub.add_parser("inspect", help="Vẽ bbox lên ảnh để kiểm tra")
    p.add_argument("dossier_dir")
    p.set_defaults(func=cmd_inspect)

    args = parser.parse_args(argv)
    if getattr(args, "no_render", False):
        args.noise = ""
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
