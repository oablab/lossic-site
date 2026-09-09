#!/usr/bin/env python3
"""Per-note OG card for lossic.app dev notes: 1200x630 sage-gradient card.

Layout measured from deepsrt.com (margin 75, icon 78 at y=63, headline lines,
subtitle, domain). Hue is Lossic's sage. Reuses the from-scratch approach in
connect-site/scripts/og_cards.py but standalone so lossic-site owns it.

Notes are registered in NOTES below (slug dir -> two headline lines + subtitle),
so regenerating every card is one run and adding a note is one entry.

    python3 scripts/og_note_card.py            # rebuild all registered notes
    python3 scripts/og_note_card.py <slug-dir> # rebuild just one
"""
import pathlib, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H = 1200, 630
MARGIN = 75
TEXT_R = 820
ICON_XY, ICON_PX = (75, 63), 78
HEAD_Y1, HEAD_Y2 = 250, 326
SUB_Y, DOMAIN_Y = 424, 557

# Lossic sage, in a comfortable luminance range (deep sage -> near-black green).
GRAD_TOP, GRAD_BOTTOM = (0x33, 0x3B, 0x2B), (0x10, 0x14, 0x0C)
INK = (0xF6, 0xF5, 0xEE)
MUTED = (0xC2, 0xCC, 0xA9)
ACCENT = (0xA8, 0xB3, 0x94)

LATIN = "/System/Library/Fonts/HelveticaNeue.ttc"
MONO = "/System/Library/Fonts/SFNSMono.ttf"
GB = "/System/Library/Fonts/Hiragino Sans GB.ttc"
BOLD = {LATIN: 1, GB: 2}
DOMAIN = "lossic.app"
WORDMARK = "Lossic"

# Registered notes: slug dir -> (two headline lines, subtitle). Add a note here
# and its card regenerates with the rest.
NOTES = {
    "zh/notes/digital-archival-stance": (
        ["關於「數位典藏」：", "Lossic 的立場與願景"],
        "我們不取代 EAC／XLD——誠實談限制，以及抓軌之後的願景。"),
    "zh/notes/share-custom-albums": (
        ["自訂專輯，", "能分享給朋友嗎？"],
        "在 drive.file 最小權限下設計「分享 → 匯入」的產品思考。"),
}


def font(path, size, bold=False):
    idx = BOLD.get(path, 0) if bold else 0
    try:
        return ImageFont.truetype(path, size, index=idx)
    except OSError:
        return ImageFont.truetype(path, size)


def width(d, t, f):
    return d.textbbox((0, 0), t, font=f)[2]


def fit(d, lines, path, start, floor, limit):
    for size in range(start, floor - 1, -1):
        f = font(path, size, bold=True)
        if all(MARGIN + width(d, l, f) <= limit for l in lines):
            return f, size
    return font(path, floor, bold=True), floor


def gradient():
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)],
               fill=tuple(round(GRAD_TOP[i] + (GRAD_BOTTOM[i] - GRAD_TOP[i]) * t)
                          for i in range(3)))
    return im


def build(dest_dir, head, sub):
    im = gradient()
    d = ImageDraw.Draw(im)

    icon = Image.open(ROOT / "icon.png").convert("RGBA")
    mark = icon.resize((ICON_PX, ICON_PX), Image.LANCZOS)
    im.paste(mark, ICON_XY, mark)

    wf = font(LATIN, 31, bold=True)
    wy = ICON_XY[1] + ICON_PX // 2 - d.textbbox((0, 0), WORDMARK, font=wf)[3] // 2 - 3
    d.text((ICON_XY[0] + ICON_PX + 18, wy), WORDMARK, font=wf, fill=INK)

    hf, hsize = fit(d, head, GB, 52, 34, TEXT_R)
    d.text((MARGIN, HEAD_Y1), head[0], font=hf, fill=INK)
    d.text((MARGIN, HEAD_Y2 if hsize > 44 else HEAD_Y1 + hsize + 22),
           head[1], font=hf, fill=INK)

    ssize = 25
    sf = font(GB, ssize)
    while MARGIN + width(d, sub, sf) > TEXT_R and ssize > 17:
        ssize -= 1
        sf = font(GB, ssize)
    d.text((MARGIN, SUB_Y), sub, font=sf, fill=MUTED)
    d.text((MARGIN, DOMAIN_Y), DOMAIN, font=font(MONO, 26), fill=ACCENT)

    dest = ROOT / dest_dir / "og-card.png"
    im.save(dest, optimize=True)
    over = [l for l in head if MARGIN + width(d, l, hf) > TEXT_R]
    if MARGIN + width(d, sub, sf) > TEXT_R:
        over.append(sub)
    import hashlib
    h = hashlib.md5(dest.read_bytes()).hexdigest()[:8]
    print(f"  {dest.relative_to(ROOT)} {im.size[0]}x{im.size[1]} {im.mode} "
          f"head={hsize}px sub={ssize}px v={h}" + ("  OVERFLOW %s" % over if over else "  ok"))


if __name__ == "__main__":
    slugs = [sys.argv[1]] if len(sys.argv) > 1 else list(NOTES)
    for slug in slugs:
        head, sub = NOTES[slug]
        build(slug, head, sub)

