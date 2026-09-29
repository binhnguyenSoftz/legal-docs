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


def _era(born: int | None) -> dict:
    """Thói quen đặt tên theo thế hệ: người lớn tuổi hay có tên đệm Thị/Văn và tên cũ, người trẻ hay có tên 4 chữ."""
    if born is None:
        return {"thi_van": (0.35, 0.2), "old_name": 0.0, "four": 0.15}
    if born < 1950:
        return {"thi_van": (0.85, 0.6), "old_name": 0.3, "four": 0.02}
    if born < 1970:
        return {"thi_van": (0.7, 0.45), "old_name": 0.12, "four": 0.05}
    if born < 1990:
        return {"thi_van": (0.4, 0.25), "old_name": 0.02, "four": 0.15}
    return {"thi_van": (0.12, 0.08), "old_name": 0.0, "four": 0.35}


def generate(rng: random.Random, gender: str, ho: str | None = None, born: int | None = None) -> dict:
    """born: năm sinh, để đặt tên đúng thế hệ. Tên 4 chữ có hai tên đệm (Nguyễn Thị Thu Hà)."""
    suffix = "nu" if gender == "female" else "nam"
    era = _era(born)
    ho = ho or _pick(rng, "ho.txt")
    if era["old_name"] and rng.random() < era["old_name"]:
        ten = _pick(rng, f"ten_{suffix}_xua.txt")
    else:
        ten = _pick(rng, f"ten_{suffix}.txt")
    classic = "Thị" if gender == "female" else "Văn"
    if rng.random() < era["thi_van"][0 if gender == "female" else 1]:
        middles = [classic]
    else:
        middles = [_pick(rng, f"ten_dem_{suffix}.txt")]
    if rng.random() < era["four"] or len(ho.split()) > 1 and rng.random() < 0.5:
        second = _pick(rng, f"ten_dem_{suffix}.txt")
        if second not in middles and second != classic:
            middles.append(second)
    middles = [m for m in middles if m != ten] or [classic if ten != classic else _pick(rng, f"ten_dem_{suffix}.txt")]
    ten_dem = " ".join(middles)
    return {"ho": ho, "ten_dem": ten_dem, "ten": ten, "ho_ten": f"{ho} {ten_dem} {ten}"}


def ascii_fold(text: str) -> str:
    """'Nguyễn Văn Đức' -> 'Nguyen Van Duc' (dùng cho MRZ)."""
    text = text.replace("Đ", "D").replace("đ", "d")
    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")
