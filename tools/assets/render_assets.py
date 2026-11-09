"""Render the README hero banner and logo PNGs with Pillow (flat colours, no gradients).

Usage:  python3 tools/assets/render_assets.py
Outputs: assets/hero-banner.png (2560x820), assets/discord-icon-512.png, assets/logo-1024.png

The vector logo is assets/logo.svg; keep draw_logo() in sync with its shapes.
The example post in the banner is fictional (MOCK).
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets"
FONT_DIR = Path("/usr/share/fonts/truetype/noto")
REGULAR, BOLD = FONT_DIR / "NotoSans-Regular.ttf", FONT_DIR / "NotoSans-Bold.ttf"

INK, MUTED, BG, LINE, NAVY, TAG, LINK = "#1F2937", "#6B7280", "#F4F6F8", "#E5E7EB", "#1F2A44", "#4B5563", "#3B5BDB"
# (fill, border, text) per label colour
MINT = ("#D5F2E1", "#8FD1A9", "#1F6B45")
AMBER = ("#FCEBC0", "#E8C468", "#8A5A00")
CORAL = ("#FAD7CF", "#EE9A8C", "#9B3B2E")
LAV = ("#E6E0F8", "#B9AEE9", "#5B4A9E")
SLATE = ("#E5E9EE", "#B7C0CB", "#475569")


def draw_logo(size):
    """Logo on a full-bleed navy square, drawn on the 512-unit grid of assets/logo.svg."""
    k = size / 512
    img = Image.new("RGB", (size, size), NAVY)
    d = ImageDraw.Draw(img)

    def rr(x, y, w, h, r, fill):
        d.rounded_rectangle([x * k, y * k, (x + w) * k, (y + h) * k], r * k, fill=fill)

    rr(96, 120, 320, 244, 40, "#FFFFFF")
    rr(140, 170, 232, 24, 12, "#D9DEE6")
    rr(132, 214, 160, 40, 10, "#F4C95D")
    rr(148, 226, 128, 16, 8, "#C4A04A")  # #8A5A00 at 55% over #F4C95D
    rr(306, 222, 66, 24, 12, "#D9DEE6")
    rr(140, 274, 150, 24, 12, "#D9DEE6")
    d.ellipse([(370 - 78) * k, (356 - 78) * k, (370 + 78) * k, (356 + 78) * k], fill=NAVY)
    d.ellipse([(370 - 64) * k, (356 - 64) * k, (370 + 64) * k, (356 + 64) * k], fill="#8E7CDB")
    rr(336, 334, 68, 13, 6.5, "#FFFFFF")
    rr(336, 365, 68, 13, 6.5, "#FFFFFF")
    # slash: a 14x84 bar rotated 28 degrees about (370, 356), with round caps
    t = math.radians(28)
    dx, dy = 35 * math.sin(t), 35 * math.cos(t)
    p1, p2 = (370 + dx, 356 - dy), (370 - dx, 356 + dy)
    d.line([p1[0] * k, p1[1] * k, p2[0] * k, p2[1] * k], fill="#FFFFFF", width=round(14 * k))
    for px, py in (p1, p2):
        d.ellipse([(px - 7) * k, (py - 7) * k, (px + 7) * k, (py + 7) * k], fill="#FFFFFF")
    return img


class Canvas:
    """Draws in 1x design units onto an R-times supersampled image."""

    def __init__(self, w, h, r):
        self.r = r
        self.img = Image.new("RGB", (w * r, h * r), BG)
        self.d = ImageDraw.Draw(self.img)
        self._fonts = {}

    def font(self, size, bold=False):
        key = (size, bold)
        if key not in self._fonts:
            self._fonts[key] = ImageFont.truetype(str(BOLD if bold else REGULAR), round(size * self.r))
        return self._fonts[key]

    def width(self, s, size, bold=False):
        return self.font(size, bold).getlength(s) / self.r

    def text(self, x, baseline, s, size, fill, bold=False, anchor="ls"):
        self.d.text((x * self.r, baseline * self.r), s, font=self.font(size, bold), fill=fill, anchor=anchor)

    def rrect(self, x, y, w, h, rad, fill=None, outline=None, stroke=0):
        r = self.r
        self.d.rounded_rectangle([x * r, y * r, (x + w) * r, (y + h) * r], rad * r, fill=fill,
                                 outline=outline, width=round(stroke * r) if outline else 0)

    def shadow(self, x, y, w, h, rad, dy, blur, alpha):
        r = self.r
        layer = Image.new("L", self.img.size, 0)
        ImageDraw.Draw(layer).rounded_rectangle([x * r, (y + dy) * r, (x + w) * r, (y + h + dy) * r], rad * r, fill=alpha)
        layer = layer.filter(ImageFilter.GaussianBlur(blur * r))
        self.img.paste(Image.new("RGB", self.img.size, "#111827"), (0, 0), layer)
        self.d = ImageDraw.Draw(self.img)

    def chip(self, x, y, label, pal, size=14, h=28):
        fill, border, txt = pal
        w = 12 + 8 + 7 + self.width(label, size, True) + 12
        self.rrect(x, y, w, h, h / 2, fill=fill, outline=border, stroke=1.5)
        cx, cy = x + 12 + 4, y + h / 2
        self.d.ellipse([(cx - 4) * self.r, (cy - 4) * self.r, (cx + 4) * self.r, (cy + 4) * self.r], fill=txt)
        self.text(x + 12 + 8 + 7, y + h / 2 + size * 0.36, label, size, txt, bold=True)
        return w

    def wrap(self, s, size, max_w, bold=False):
        lines, cur = [], ""
        for word in s.split():
            trial = f"{cur} {word}".strip()
            if self.width(trial, size, bold) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        return lines + [cur]


def hero():
    W, H, R = 1280, 410, 4
    c = Canvas(W, H, R)

    # Left: brand, title, tagline, legend chips, credits
    icon = draw_logo(40 * R)
    mask = Image.new("L", icon.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, icon.size[0] - 1, icon.size[1] - 1], 10 * R, fill=255)
    c.img.paste(icon, (64 * R, 52 * R), mask)
    c.text(116, 77, "BROWSER EXTENSION  ·  AI FOR GOOD", 15, MUTED, bold=True)
    c.text(64, 156, "Inline Evidence", 48, INK, bold=True)
    c.text(64, 210, "Highlights", 48, INK, bold=True)
    for i, line in enumerate(c.wrap("See exactly where a post differs from its source, with the evidence one hover away.", 21, 540)):
        c.text(64, 252 + i * 30, line, 21, TAG)
    x = 64
    for label, pal in (("Matches", MINT), ("Changed", AMBER), ("Contradicts", CORAL), ("Outdated", LAV), ("Not found", SLATE)):
        x += c.chip(x, 314, label, pal) + 8
    c.text(64, 384, "Le Tuan · Lok Sang · Truyen Anh — AI Builders Challenge, North America 2026", 14, MUTED)

    # Right: example post (MOCK)
    px, py, pw = 672, 44, 548
    ph = 216
    c.shadow(px, py, pw, ph, 16, 6, 8, 22)
    c.rrect(px, py, pw, ph, 16, fill="#FFFFFF", outline=LINE, stroke=1)
    ax, ay = px + 22 + 20, py + 20 + 20
    c.d.ellipse([(ax - 20) * R, (ay - 20) * R, (ax + 20) * R, (ay + 20) * R], fill="#DCE7F3")
    c.text(ax, ay, "SD", 14, "#3B5275", bold=True, anchor="mm")
    c.text(px + 74, 80, "Science Digest", 15, INK, bold=True)
    c.text(px + 74, 99, "2h · shared a link", 13, MUTED)

    size = 22
    parts = [("Coffee ", None), ("prevents", AMBER), (" Alzheimer's, ", None), ("new study", LAV), (" shows.", None)]
    while sum(c.width(s, size) for s, _ in parts) + 12 > pw - 44:
        size -= 1
    base, x = 140, px + 22
    hl = None
    for s, pal in parts:
        w = c.width(s, size)
        if pal:
            top, bot = base - size * 0.98, base + size * 0.30
            c.rrect(x - 3, top, w + 6, bot - top, 4, fill=pal[0])
            c.d.rectangle([(x - 1) * R, (bot - 2) * R, (x + w + 1) * R, bot * R], fill=pal[1])
            if pal is AMBER:
                hl = (x - 3, top, x + w + 3, bot)
            c.text(x, base, s, size, INK)
            x += w + 6 if pal else w
            continue
        c.text(x, base, s, size, INK)
        x += w

    lx, ly, lw, lh = px + 22, 162, pw - 44, 76
    c.rrect(lx, ly, lw, lh, 10, fill="#F9FAFB", outline=LINE, stroke=1)
    c.text(lx + 14, ly + 24, "JOURNAL.EXAMPLE", 12, MUTED)
    c.text(lx + 14, ly + 45, "Caffeine intake and amyloid pathology in aged mice", 15, INK, bold=True)
    c.text(lx + 14, ly + 65, "Published 2019", 13, MUTED)

    # Hover evidence card anchored under the amber highlight
    cw, chh = lw, 170  # overlay spans the link preview, like a real hover card
    cx = lx
    cy = hl[3] + 12
    c.shadow(cx, cy, cw, chh, 14, 10, 12, 40)
    c.rrect(cx, cy, cw, chh, 14, fill="#FFFFFF", outline=AMBER[1], stroke=1.5)
    tx = hl[0] + 18  # caret points at the highlight
    caret = [(tx * R, (cy - 8) * R), ((tx + 9) * R, (cy + 1) * R), ((tx - 9) * R, (cy + 1) * R)]
    c.d.polygon(caret, fill="#FFFFFF")
    c.d.line([caret[2], caret[0], caret[1]], fill=AMBER[1], width=round(1.5 * R))
    w = c.chip(cx + 16, cy + 14, "Changed from source", AMBER)
    c.text(cx + 16 + w + 10, cy + 33, "Causality strengthened", 13, MUTED, bold=True)
    col1 = 120
    c2x = cx + 16 + col1 + 12
    c.text(cx + 16, cy + 66, "POST", 11, MUTED, bold=True)
    c.text(c2x, cy + 66, "SOURCE", 11, MUTED, bold=True)
    c.text(cx + 16, cy + 87, "“prevents”", 15, INK)
    for i, line in enumerate(c.wrap("“was associated with a lower incidence of”", 15, cw - 16 - (c2x - cx))):
        c.text(c2x, cy + 87 + i * 21, line, 15, INK)
    c.rrect(cx + 16, cy + 104, cw - 32, 30, 8, fill=SLATE[0])
    c.text(cx + 26, cy + 124, "Context: study in aged mice", 13, SLATE[2])
    c.text(cx + 16, cy + 156, "journal.example · 2019", 13, MUTED)
    c.text(cx + cw - 16, cy + 156, "Open evidence ›", 13, LINK, bold=True, anchor="rs")

    # Pointer resting on the highlight
    ox, oy, s = hl[2] - 7, hl[1] + 17, 0.95
    pts = [(3, 2), (3, 19), (8, 14.5), (11.5, 22), (14.5, 20.7), (11, 13.3), (18, 13.3)]
    poly = [((ox + px_ * s) * R, (oy + py_ * s) * R) for px_, py_ in pts]
    c.d.polygon(poly, fill="#111827", outline="#FFFFFF", width=round(1.6 * R))

    out = c.img.resize((W * 2, H * 2), Image.LANCZOS)
    out.save(OUT / "hero-banner.png", optimize=True)


def main():
    OUT.mkdir(exist_ok=True)
    big = draw_logo(2048)
    big.resize((512, 512), Image.LANCZOS).save(OUT / "discord-icon-512.png", optimize=True)
    big.resize((1024, 1024), Image.LANCZOS).save(OUT / "logo-1024.png", optimize=True)
    hero()
    for name in ("hero-banner.png", "discord-icon-512.png", "logo-1024.png"):
        with Image.open(OUT / name) as im:
            print(name, im.size, f"{(OUT / name).stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
