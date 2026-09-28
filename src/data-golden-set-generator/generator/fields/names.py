import random
import unicodedata
from functools import cache

from generator import RESOURCES_DIR


@cache
def _load(name: str) -> tuple[list[str], list[float]]:
    items, weights = [], []
    for line in (RESOURCES_DIR / "names" / name).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        value, _, weight = line.partition("\t")
        items.append(value.strip())
        weights.append(float(weight) if weight else 1.0)
    return items, weights


def _pick(rng: random.Random, name: str) -> str:
    items, weights = _load(name)
    return rng.choices(items, weights=weights, k=1)[0]


def generate(rng: random.Random, gender: str, ho: str | None = None) -> dict:
    suffix = "nu" if gender == "female" else "nam"
    ho = ho or _pick(rng, "ho.txt")
    ten = _pick(rng, f"ten_{suffix}.txt")
    ten_dem = _pick(rng, f"ten_dem_{suffix}.txt")
    while ten_dem == ten:
        ten_dem = _pick(rng, f"ten_dem_{suffix}.txt")
    return {"ho": ho, "ten_dem": ten_dem, "ten": ten, "ho_ten": f"{ho} {ten_dem} {ten}"}


def ascii_fold(text: str) -> str:
    """'Nguyễn Văn Đức' -> 'Nguyen Van Duc' (dùng cho MRZ)."""
    text = text.replace("Đ", "D").replace("đ", "d")
    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")
