"""Thêm nhiễu cho ảnh trang sạch, giữ bbox đúng sau biến đổi.

Thứ tự: dấu/chữ ký -> hiệu ứng giấy/mực (Augraphy) -> hình học (xoay, phối cảnh, nền bàn)
-> hiệu ứng máy ảnh (mờ, hạt, JPEG).
Biến đổi hình học tự làm bằng một ma trận homography để biến đổi bbox theo cùng ma trận.
"""

import contextlib
import random
import tempfile
from functools import cache
from pathlib import Path

import cv2
import numpy as np

from generator import RESOURCES_DIR

LEVELS = {
    "light": {"rotate": 1.0, "perspective": 0.0, "blur": 0.6, "grain": 3, "jpeg": (80, 95),
              "augraphy": False, "overlay": 0.3, "background": 0.0},
    "medium": {"rotate": 3.0, "perspective": 0.02, "blur": 1.2, "grain": 8, "jpeg": (60, 85),
               "augraphy": True, "overlay": 0.6, "background": 0.2},
    "heavy": {"rotate": 7.0, "perspective": 0.06, "blur": 2.0, "grain": 14, "jpeg": (40, 70),
              "augraphy": True, "overlay": 0.9, "background": 0.8},
}


def _pngs(folder: str) -> list[Path]:
    return sorted((RESOURCES_DIR / folder).glob("*.png"))


def _overlay(rng: random.Random, img: np.ndarray, boxes: dict, ops: list[str]) -> np.ndarray:
    """Chèn dấu/chữ ký, có lúc đè lên một trường. Ảnh nguồn phải có kênh alpha."""
    candidates = _pngs("stamps") + _pngs("signatures")
    if not candidates:
        return img
    src = cv2.imread(str(rng.choice(candidates)), cv2.IMREAD_UNCHANGED)
    if src is None or src.shape[2] != 4:
        return img
    h, w = img.shape[:2]
    target = min(h, w) * rng.uniform(0.15, 0.25)
    k = target / max(src.shape[:2])
    src = cv2.resize(src, None, fx=k, fy=k)
    sh, sw = src.shape[:2]
    all_boxes = [b for bs in boxes.values() for b in bs]
    if all_boxes and rng.random() < 0.5:
        b = rng.choice(all_boxes)
        x, y = int(b["x"] + b["w"] / 2 - sw / 2), int(b["y"] + b["h"] / 2 - sh / 2)
        ops.append("overlay:on_field")
    else:
        x, y = rng.randint(0, max(0, w - sw)), rng.randint(int(h * 0.6), max(int(h * 0.6), h - sh))
        ops.append("overlay")
    x, y = max(0, min(x, w - sw)), max(0, min(y, h - sh))
    alpha = src[:, :, 3:4] / 255.0
    roi = img[y:y + sh, x:x + sw]
    img[y:y + sh, x:x + sw] = (roi * (1 - alpha) + src[:, :, :3] * alpha).astype(np.uint8)
    return img


def _augraphy_pipeline(level: str):
    """Chỉ dùng phép không đổi hình học/kích thước ảnh, để bbox vẫn đúng.

    Không dùng Letterpress: làm mất tương phản chữ tới mức không đọc được.
    Không dùng default_augraphy_pipeline(): có BookBinding, PageBorder, Folding... làm đổi kích thước ảnh
    (lệch bbox) và có phép lỗi ngẫu nhiên trên Python >= 3.12 (random.randint nhận float).
    """
    import augraphy as A

    ink = [A.InkBleed(p=0.5), A.LowInkRandomLines(p=0.4), A.LowInkPeriodicLines(p=0.3)]
    paper = [A.NoiseTexturize(p=0.5), A.BrightnessTexturize(p=0.4)]
    post = [A.DirtyDrum(p=0.2), A.LightingGradient(p=0.3)]
    if level == "heavy":
        paper.append(A.Stains(p=0.3))
        post += [A.BadPhotoCopy(p=0.2), A.ShadowCast(p=0.3)]
    return A.AugraphyPipeline(ink_phase=ink, paper_phase=paper, post_phase=post)


@cache
def _scratch_dir() -> tempfile.TemporaryDirectory:
    """AugraphyPipeline luôn ghi ảnh vào <cwd>/augraphy_cache/ (không tắt được). Cho nó ghi vào thư mục tạm, tự xóa khi thoát."""
    return tempfile.TemporaryDirectory(prefix="augraphy_")


def _augraphy(img: np.ndarray, seed: int, level: str, ops: list[str]) -> np.ndarray:
    try:
        pipeline = _augraphy_pipeline(level)
    except ImportError:
        return img
    random.seed(seed)
    np.random.seed(seed % 2**32)
    try:
        with contextlib.chdir(_scratch_dir().name):
            out = pipeline(img)
    except Exception as e:  # Lỗi của augraphy không được làm hỏng cả lô sinh
        ops.append(f"augraphy:error:{type(e).__name__}")
        return img
    if out.ndim == 2:
        out = cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)
    if out.shape[:2] != img.shape[:2]:
        ops.append("augraphy:skipped_shape_change")
        return img
    ops.append(f"augraphy:{level}")
    return out


def _homography(rng: random.Random, w: int, h: int, cfg: dict, ops: list[str]) -> tuple[np.ndarray, tuple[int, int]]:
    angle = rng.uniform(-cfg["rotate"], cfg["rotate"])
    rot = np.vstack([cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0), [0, 0, 1]])
    ops.append(f"rotate:{angle:.2f}")
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    j = cfg["perspective"] * min(w, h)
    dst = np.float32([[x + rng.uniform(-j, j), y + rng.uniform(-j, j)] for x, y in src])
    persp = cv2.getPerspectiveTransform(src, dst)
    if j:
        ops.append(f"perspective:{cfg['perspective']}")
    H = persp @ rot
    # Dịch để toàn bộ trang nằm trong khung, chừa lề cho nền.
    corners = cv2.perspectiveTransform(src[None], H)[0]
    pad = int(0.08 * max(w, h)) if cfg.get("_background") else 0
    min_xy = corners.min(axis=0)
    shift = np.array([[1, 0, pad - min_xy[0]], [0, 1, pad - min_xy[1]], [0, 0, 1]])
    size = corners.max(axis=0) - min_xy + 2 * pad
    return shift @ H, (int(np.ceil(size[0])), int(np.ceil(size[1])))


def _transform_boxes(boxes: dict, H: np.ndarray) -> dict:
    out = {}
    for name, bs in boxes.items():
        out[name] = []
        for b in bs:
            pts = np.float32([[b["x"], b["y"]], [b["x"] + b["w"], b["y"]],
                              [b["x"] + b["w"], b["y"] + b["h"]], [b["x"], b["y"] + b["h"]]])
            t = cv2.perspectiveTransform(pts[None], H)[0]
            (x0, y0), (x1, y1) = t.min(axis=0), t.max(axis=0)
            out[name].append({"page": b["page"], "x": round(float(x0), 1), "y": round(float(y0), 1),
                              "w": round(float(x1 - x0), 1), "h": round(float(y1 - y0), 1)})
    return out


def apply(clean_png: Path, boxes: dict, level: str, seed: int, out_path: Path) -> dict:
    """boxes: name -> list bbox của trang này. Trả về bản ghi cho files.noisy."""
    rng = random.Random(seed)
    cfg = dict(LEVELS[level])
    ops: list[str] = []
    img = cv2.imread(str(clean_png), cv2.IMREAD_COLOR)

    if rng.random() < cfg["overlay"]:
        img = _overlay(rng, img, boxes, ops)
    if cfg["augraphy"]:
        img = _augraphy(img, seed, level, ops)

    backgrounds = sorted((RESOURCES_DIR / "backgrounds").glob("*.jpg"))
    cfg["_background"] = bool(backgrounds) and rng.random() < cfg["background"]
    h, w = img.shape[:2]
    H, size = _homography(rng, w, h, cfg, ops)
    if cfg["_background"]:
        bg = cv2.resize(cv2.imread(str(rng.choice(backgrounds))), size)
        img = cv2.warpPerspective(img, H, size, dst=bg, borderMode=cv2.BORDER_TRANSPARENT)
        ops.append("background")
    else:
        img = cv2.warpPerspective(img, H, size, borderValue=(255, 255, 255))
    new_boxes = _transform_boxes(boxes, H)

    sigma = rng.uniform(0, cfg["blur"])
    if sigma > 0.2:
        img = cv2.GaussianBlur(img, (0, 0), sigma)
        ops.append(f"blur:{sigma:.2f}")
    if cfg["grain"]:
        grain = np.random.default_rng(seed).normal(0, cfg["grain"], img.shape)
        img = np.clip(img + grain, 0, 255).astype(np.uint8)
        ops.append(f"grain:{cfg['grain']}")
    quality = rng.randint(*cfg["jpeg"])
    cv2.imwrite(str(out_path), img, [cv2.IMWRITE_JPEG_QUALITY, quality])
    ops.append(f"jpeg:{quality}")
    return {"level": level, "path": out_path.name, "ops": ops, "bboxes": new_boxes}
