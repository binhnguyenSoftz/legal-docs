"""Render thật bằng Chromium. Bỏ qua nếu chưa cài: pip install -e ".[render]" && playwright install chromium."""

import random

import pytest

from generator import dossier, spec
from generator.rng import derive_seed

pytest.importorskip("playwright")


@pytest.fixture(scope="module")
def renderer():
    from generator.render import Renderer
    try:
        r = Renderer(dpi=96)
    except Exception as e:  # Chưa tải Chromium
        pytest.skip(f"Không mở được Chromium: {e}")
    yield r
    r.close()


@pytest.mark.parametrize("index", [0, 1])
def test_every_printed_field_has_bbox(renderer, tmp_path, index):
    from generator.render import pick_style
    proc = spec.load_procedure("giai-toa-den-bu")
    d = dossier.build(proc, 3, index)
    style = pick_style(random.Random(derive_seed(d["seed"], "style")))
    for doc in d["documents"]:
        renderer.render(proc.name, doc, d, style, tmp_path)
        assert doc["files"]["pages"], doc["doc_id"]
        missing = [n for n, f in doc["fields"].items() if f["text"] and not f["bbox"]]
        assert missing == [], f"{doc['doc_id']}: trường có chữ nhưng không có trên trang: {missing}"
        pages = len(doc["files"]["pages"])
        assert all(1 <= b["page"] <= pages for f in doc["fields"].values() for b in f["bbox"])
