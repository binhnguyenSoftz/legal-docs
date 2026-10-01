"""HTML (Jinja2) -> PDF + PNG từng trang + bbox từng trường, bằng Playwright/Chromium.

Template chia trang bằng <section class="page"> cố định khổ A4 (xem _shared/base.css),
nên ảnh chụp từng section khớp đúng trang PDF và bbox dùng được cho cả hai.
"""

import random
from pathlib import Path

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup

from generator import RESOURCES_DIR, TEMPLATES_DIR, spec, style
from generator.rng import derive_seed

CSS_DPI = 96

_BBOX_JS = """
() => {
  // Mỗi dòng chữ của một trường là một bbox: trường xuống dòng (địa chỉ dài) cho nhiều bbox, không phải một khối trùm cả đoạn.
  const lineRects = el => {
    const range = document.createRange();
    range.selectNodeContents(el);
    const rects = [...range.getClientRects()].filter(r => r.width > 0.5 && r.height > 0.5);
    const lines = [];
    for (const r of rects) {
      const same = lines.find(l => Math.abs(l.top - r.top) < r.height / 2);
      if (same) {
        same.left = Math.min(same.left, r.left); same.right = Math.max(same.right, r.right);
        same.top = Math.min(same.top, r.top); same.bottom = Math.max(same.bottom, r.bottom);
      } else lines.push({left: r.left, right: r.right, top: r.top, bottom: r.bottom});
    }
    // Trường trống: giữ khung ô điền để biết vị trí.
    return lines.length ? lines : [el.getBoundingClientRect()];
  };
  const pages = [...document.querySelectorAll('section.page')];
  const out = {};
  pages.forEach((page, i) => {
    const p = page.getBoundingClientRect();
    page.querySelectorAll('[data-field]').forEach(el => {
      const rects = el instanceof SVGElement ? [el.getBoundingClientRect()] : lineRects(el);
      for (const r of rects) {
        (out[el.dataset.field] ||= []).push({page: i + 1, x: r.left - p.left, y: r.top - p.top,
                                             w: r.right - r.left, h: r.bottom - r.top});
      }
    });
  });
  return {pages: pages.length, fields: out, text: pages.map(p => p.innerText)};
}
"""


def signature_svg(key: str, width: int = 140, height: int = 50) -> Markup:
    """Chữ ký giả: vài nét cong ngẫu nhiên, cố định theo key."""
    rng = random.Random(derive_seed(0, "signature", key))
    x, y = rng.uniform(5, 20), rng.uniform(height * 0.4, height * 0.7)
    d = [f"M{x:.1f},{y:.1f}"]
    for _ in range(rng.randint(4, 7)):
        x2 = min(width - 5, x + rng.uniform(10, 30))
        d.append(f"C{x + rng.uniform(-10, 15):.1f},{rng.uniform(0, height):.1f} "
                 f"{x2 - rng.uniform(-10, 15):.1f},{rng.uniform(0, height):.1f} {x2:.1f},{rng.uniform(height * 0.3, height * 0.8):.1f}")
        x = x2
    d.append(f"M{rng.uniform(10, 30):.1f},{height * 0.8:.1f} L{rng.uniform(width * 0.6, width - 5):.1f},{height * rng.uniform(0.65, 0.9):.1f}")
    return Markup(f'<svg class="signature" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
                  f'<path d="{" ".join(d)}" fill="none" stroke="var(--hw-color)" stroke-width="1.6" stroke-linecap="round"/></svg>')


def stamp_svg(key: str, size: int = 130) -> Markup:
    """Dấu tròn giả lập. Chữ trên dấu cố ý ghi MẪU GIẢ LẬP, không mô phỏng dấu thật của cơ quan nào."""
    rng = random.Random(derive_seed(0, "stamp", key))
    r = size / 2
    rot = rng.uniform(-25, 25)
    text = "MẪU GIẢ LẬP ★ KHÔNG CÓ GIÁ TRỊ PHÁP LÝ ★"
    return Markup(
        f'<svg class="stamp" width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="transform: rotate({rot:.1f}deg)">'
        f'<defs><path id="ring-{key}" d="M{r},{r} m-{r * 0.72},0 a{r * 0.72},{r * 0.72} 0 1,1 {r * 1.44},0 a{r * 0.72},{r * 0.72} 0 1,1 -{r * 1.44},0"/></defs>'
        f'<circle cx="{r}" cy="{r}" r="{r - 3}" fill="none" stroke="#c8102e" stroke-width="3"/>'
        f'<circle cx="{r}" cy="{r}" r="{r * 0.55}" fill="none" stroke="#c8102e" stroke-width="1.2"/>'
        f'<text font-size="{size * 0.085:.1f}" fill="#c8102e" font-weight="bold"><textPath href="#ring-{key}">{text}</textPath></text>'
        f'<text x="{r}" y="{r + size * 0.06:.1f}" text-anchor="middle" font-size="{size * 0.18:.1f}" fill="#c8102e">★</text></svg>')


def qr_svg(key: str, size: int = 60, cells: int = 25) -> Markup:
    """Ô vuông giống mã QR (không mã hóa gì), để có vùng nhiễu thị giác như thẻ thật."""
    rng = random.Random(derive_seed(0, "qr", key))
    c = size / cells
    finder = [(0, 0), (cells - 7, 0), (0, cells - 7)]

    def in_finder(x, y):
        return any(fx <= x < fx + 7 and fy <= y < fy + 7 for fx, fy in finder)
    rects = [f'<rect x="{x * c:.2f}" y="{y * c:.2f}" width="{c:.2f}" height="{c:.2f}"/>'
             for y in range(cells) for x in range(cells) if not in_finder(x, y) and rng.random() < 0.5]
    for fx, fy in finder:
        rects.append(f'<rect x="{(fx + 0.5) * c:.2f}" y="{(fy + 0.5) * c:.2f}" width="{6 * c:.2f}" height="{6 * c:.2f}" fill="none" stroke="#000" stroke-width="{c:.2f}"/>')
        rects.append(f'<rect x="{(fx + 2) * c:.2f}" y="{(fy + 2) * c:.2f}" width="{3 * c:.2f}" height="{3 * c:.2f}"/>')
    return Markup(f'<svg class="qr" width="{size}" height="{size}" viewBox="0 0 {size} {size}">{"".join(rects)}</svg>')


def barcode_svg(key: str, width: int = 120, height: int = 22) -> Markup:
    rng = random.Random(derive_seed(0, "barcode", key))
    x, bars = 0.0, []
    while x < width:
        w = rng.choice([0.8, 0.8, 1.6, 2.4])
        if rng.random() < 0.55:
            bars.append(f'<rect x="{x:.1f}" y="0" width="{w}" height="{height}"/>')
        x += w
    return Markup(f'<svg class="barcode" width="{width}" height="{height}" viewBox="0 0 {width} {height}">{"".join(bars)}</svg>')


def environment() -> Environment:
    """Tìm template ở thư mục thủ tục đang dùng (spec.TEMPLATES_DIR, test có thể đổi) rồi tới templates/ gốc (_shared)."""
    loader = ChoiceLoader([FileSystemLoader(spec.TEMPLATES_DIR), FileSystemLoader(TEMPLATES_DIR)])
    env = Environment(loader=loader, undefined=StrictUndefined, autoescape=True)
    env.globals.update(signature=signature_svg, stamp=stamp_svg, qr=qr_svg, barcode=barcode_svg,
                       font_faces=style.font_faces())
    return env


def pick_style(rng: random.Random) -> dict:
    """Phong cách điền tay của người khai, cố định cho cả hồ sơ."""
    fonts = sorted((RESOURCES_DIR / "fonts" / "handwriting").glob("*.[ot]tf"))
    return {
        "hw_font": fonts and rng.choice(fonts).as_uri() or None,
        "ink_color": rng.choice(["#1a2a8a", "#0d1b5e", "#222222", "#1f3fbf"]),
        "hw_size": rng.choice([13, 14, 15]),
    }


class Renderer:
    def __init__(self, dpi: int = 200):
        from playwright.sync_api import sync_playwright

        self.scale = dpi / CSS_DPI
        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch()
        self._page = self._browser.new_page(device_scale_factor=self.scale)
        self.env = environment()

    def close(self):
        self._browser.close()
        self._pw.stop()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def render(self, procedure: str, doc: dict, dossier: dict, style: dict, out_dir: Path) -> None:
        """Ghi <doc_id>.html/.pdf/_p<N>.png vào out_dir, điền doc['files'] và bbox (pixel ảnh) vào từng trường."""
        # doc["template"]: giấy tờ dùng lại từ thủ tục khác (`from` trong procedure.yaml) có template ở thư mục đó.
        template = self.env.get_template(doc.get("template") or f"{procedure}/{doc['doc_type']}/template.html.j2")
        html = template.render(doc=doc, fields=doc["fields"], persona=dossier["persona"], dossier=dossier, style=style,
                               people=dossier.get("people"), property=dossier.get("property"),
                               timeline=dossier.get("timeline"), thu_hoi=dossier.get("thu_hoi"))
        html_path = out_dir / f"{doc['doc_id']}.html"
        html_path.write_text(html, encoding="utf-8")

        page = self._page
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")

        layout = page.evaluate(_BBOX_JS)
        for name, boxes in layout["fields"].items():
            doc["fields"][name]["bbox"] = [
                {"page": b["page"], **{k: round(b[k] * self.scale, 1) for k in ("x", "y", "w", "h")}} for b in boxes
            ]

        pages = []
        for i, section in enumerate(page.query_selector_all("section.page"), start=1):
            png = out_dir / f"{doc['doc_id']}_p{i}.png"
            section.screenshot(path=png)
            pages.append(png.name)

        pdf = out_dir / f"{doc['doc_id']}.pdf"
        page.pdf(path=pdf, prefer_css_page_size=True, print_background=True)
        doc["files"] = {"html": html_path.name, "pdf": pdf.name, "pages": pages, "text": layout["text"], "noisy": []}
