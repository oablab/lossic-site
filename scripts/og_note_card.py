#!/usr/bin/env python3
"""Per-note OG card for lossic.app dev notes: 1200x630 sage-gradient card.

Layout measured from deepsrt.com (margin 75, icon 78 at y=63, headline lines,
subtitle, domain). Hue is Lossic's sage. Reuses the from-scratch approach in
connect-site/scripts/og_cards.py but standalone so lossic-site owns it.

    python3 scripts/og_note_card.py <note-slug-dir>
e.g. python3 scripts/og_note_card.py zh/notes/digital-archival-stance
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

# The one card we are drawing. Title split into two lines + a subtitle.
HEAD = ["關於「數位典藏」：", "Lossic 的立場與願景"]
SUB = "我們不取代 EAC／XLD——誠實談限制，以及抓軌之後的願景。"


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


def build(dest_dir):
    im = gradient()
    d = ImageDraw.Draw(im)

    icon = Image.open(ROOT / "icon.png").convert("RGBA")
    mark = icon.resize((ICON_PX, ICON_PX), Image.LANCZOS)
    im.paste(mark, ICON_XY, mark)

    wf = font(LATIN, 31, bold=True)
    wy = ICON_XY[1] + ICON_PX // 2 - d.textbbox((0, 0), WORDMARK, font=wf)[3] // 2 - 3
    d.text((ICON_XY[0] + ICON_PX + 18, wy), WORDMARK, font=wf, fill=INK)

    hf, hsize = fit(d, HEAD, GB, 52, 34, TEXT_R)
    d.text((MARGIN, HEAD_Y1), HEAD[0], font=hf, fill=INK)
    d.text((MARGIN, HEAD_Y2 if hsize > 44 else HEAD_Y1 + hsize + 22),
           HEAD[1], font=hf, fill=INK)

    ssize = 25
    sf = font(GB, ssize)
    while MARGIN + width(d, SUB, sf) > TEXT_R and ssize > 17:
        ssize -= 1
        sf = font(GB, ssize)
    d.text((MARGIN, SUB_Y), SUB, font=sf, fill=MUTED)
    d.text((MARGIN, DOMAIN_Y), DOMAIN, font=font(MONO, 26), fill=ACCENT)

    dest = ROOT / dest_dir / "og-card.png"
    im.save(dest, optimize=True)
    over = [l for l in HEAD if MARGIN + width(d, l, hf) > TEXT_R]
    if MARGIN + width(d, SUB, sf) > TEXT_R:
        over.append(SUB)
    print(f"  {dest.relative_to(ROOT)} {im.size[0]}x{im.size[1]} {im.mode} "
          f"head={hsize}px sub={ssize}px" + ("  OVERFLOW %s" % over if over else "  ok"))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "zh/notes/digital-archival-stance")
