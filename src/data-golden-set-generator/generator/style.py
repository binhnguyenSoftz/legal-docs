"""Hình thức hiển thị của từng giấy tờ: khổ giấy, màu giấy cũ, mực phai, vết ố, nếp gấp, font.

Đây là hình thức của bản gốc (ảnh sạch), khác với nhiễu chụp/quét ở noise.py.
Khai báo trong schema.yaml, mục `render`:

    render:
      page: a4            # a4 | a4l (A4 ngang, bảng chiết tính) | card | so (sổ hộ khẩu)
      paper: aged         # white | aged | ruled (giấy kẻ dòng)
      age: [0.3, 0.9]     # mức cũ: 0 = mới, 1 = rất cũ (ố vàng, mực phai)
      print_font: serif   # serif | typewriter | sans
      folds: [0, 2]       # số nếp gấp ngang
"""

import random

from generator import RESOURCES_DIR

PAGES = {"a4": (210, 297), "a4l": (297, 210), "card": (85.6, 53.98), "so": (125, 180)}
PRINT_FONTS = {
    "serif": ("Tinos", "Tinos-Regular.ttf", "Tinos-Bold.ttf"),
    "typewriter": ("Cousine", "Cousine-Regular.ttf", "Cousine-Bold.ttf"),
    "sans": ("Arimo", "Arimo[wght].ttf", "Arimo[wght].ttf"),
}
HW_INKS = ["#1a2a8a", "#0d1b5e", "#222222", "#1f3fbf"]


def _mix(a: str, b: str, t: float) -> str:
    """Trộn hai màu hex theo tỷ lệ t (0 -> a, 1 -> b)."""
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(ca, cb))


def font_faces() -> list[dict]:
    """@font-face cho font in. Thiếu file thì trình duyệt dùng font dự phòng trong base.css."""
    out = []
    for family, regular, bold in PRINT_FONTS.values():
        for weight, file in (("normal", regular), ("bold", bold)):
            path = RESOURCES_DIR / "fonts" / "print" / file
            if path.exists():
                out.append({"family": family, "weight": weight, "src": path.as_uri()})
    return out


def handwriting_fonts() -> list[str]:
    return [p.as_uri() for p in sorted((RESOURCES_DIR / "fonts" / "handwriting").glob("*.[ot]tf"))]


def doc_style(rng: random.Random, spec: dict) -> dict:
    page = spec.get("page", "a4")
    w, h = PAGES[page]
    paper = spec.get("paper", "white")
    lo, hi = spec.get("age", [0, 0])
    age = round(rng.uniform(lo, hi), 2) if paper != "white" or hi else 0.0
    f_lo, f_hi = spec.get("folds", [0, 0])
    stains = [{"x": rng.randint(0, 100), "y": rng.randint(0, 100), "r": rng.randint(4, 18),
               "a": round(rng.uniform(0.05, 0.22) * age, 3)} for _ in range(round(age * rng.randint(0, 6)))]
    hw_fonts = handwriting_fonts()
    hw_ink = rng.choice(HW_INKS)
    return {
        "page": page,
        "w_mm": w,
        "h_mm": h,
        "paper": paper,
        "age": age,
        "paper_color": _mix("#ffffff", "#e6d6ae", age),
        "ink": _mix("#111111", "#4a4134", age * 0.8),
        "hw_ink": _mix(hw_ink, "#5a5a78", age * 0.6),
        "hw_font": rng.choice(hw_fonts) if hw_fonts else None,
        "hw_size": rng.choice([13, 14, 15]),
        "print_font": PRINT_FONTS[spec.get("print_font", "serif")][0],
        "stains": stains,
        "folds": sorted(round(rng.uniform(25, 75), 1) for _ in range(rng.randint(f_lo, f_hi))),
        "tilt": round(rng.uniform(-0.6, 0.6), 2) if paper == "ruled" else 0.0,
    }
