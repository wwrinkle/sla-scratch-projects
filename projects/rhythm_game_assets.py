#!/usr/bin/env python3
"""Draw the costumes and backdrops for the two rhythm game starters (drum-game, melody-game).

    pip install fonttools
    python3 projects/rhythm_game_assets.py

Writes SVGs into projects/drum-game/assets/ and projects/melody-game/assets/.
Words (PERFECT!, the game titles) are drawn as shapes in the Bungee font, so they look
the same on every computer. Set BUNGEE=/path/to/Bungee-Regular.ttf if it isn't found.
"""

import os
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent
BUNGEE = Path(os.environ.get("BUNGEE", Path.home() / ".local/share/fonts/bungee/Bungee-Regular.ttf"))

# Lanes, left to right: name, colour, rotation of the up-pointing arrow, x on the Scratch stage.
# Keep the x positions in step with lane_x in Arrow.gs and Pads.gs.
LANES = [
    ("left", "#FF4FA3", -90, -75),
    ("down", "#00B4A6", 180, 10),
    ("up", "#FFC93C", 0, 95),
    ("right", "#9B5DE5", 90, 180),
]
TARGET_Y = -125  # stage y of the target line (target_y in Arrow.gs)

# An arrow pointing up in a 72 × 72 box.
ARROW = "M36 5 L66 35 L47 35 L47 66 L25 66 L25 35 L6 35 Z"


def svg(width, height, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">{body}</svg>\n')


def text_path(text, size, x, y, anchor="middle"):
    """SVG path data for text in Bungee. (x, y) is the baseline point; anchor is start/middle."""
    font = TTFont(BUNGEE)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    scale = size / font["head"].unitsPerEm
    names = [cmap[ord(ch)] for ch in text]
    width = sum(glyphs[n].width for n in names) * scale
    pen = SVGPathPen(glyphs)
    cursor = x - (width / 2 if anchor == "middle" else 0)
    for name in names:
        glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, cursor, y)))
        cursor += glyphs[name].width * scale
    return pen.getCommands()


def write(project, name, content):
    folder = ROOT / project / "assets"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_text(content)


def arrow_costume(colour, angle, fill_opacity=1):
    return svg(72, 72,
               f'<g transform="rotate({angle} 36 36)">'
               f'<path d="{ARROW}" fill="{colour}" fill-opacity="{fill_opacity}" stroke="#FFFFFF" '
               f'stroke-width="4" stroke-linejoin="round"/>'
               f'<path d="M36 13 L55 31" stroke="#FFFFFF" stroke-opacity="0.45" stroke-width="4" '
               f'stroke-linecap="round" fill="none"/></g>')


def pad_costume(colour, angle, lit):
    """A target: a tall tap zone (big enough for fingers on an iPad) with the arrow in the
    middle. Everything is see-through so the falling arrows show behind it."""
    if lit:
        zone = f'fill="{colour}" fill-opacity="0.45" stroke="#FFFFFF" stroke-width="3"'
        arrow = f'fill="#FFFFFF" stroke="{colour}" stroke-width="5"'
    else:
        zone = f'fill="{colour}" fill-opacity="0.12" stroke="{colour}" stroke-opacity="0.6" stroke-width="2"'
        arrow = f'fill="#FFFFFF" fill-opacity="0.05" stroke="{colour}" stroke-width="5"'
    return svg(82, 124,
               f'<rect x="2" y="2" width="78" height="120" rx="14" {zone}/>'
               f'<g transform="translate(5 26) rotate({angle} 36 36)">'
               f'<path d="{ARROW}" {arrow} stroke-linejoin="round"/></g>')


def judge_costume(word, colour):
    d = text_path(word, 44, 130, 52)
    return svg(260, 70,
               f'<path d="{d}" fill="none" stroke="#1B1035" stroke-width="9" stroke-linejoin="round"/>'
               f'<path d="{d}" fill="{colour}"/>')


def backdrop(title_lines):
    parts = [
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#140B2E"/><stop offset="1" stop-color="#2D1B69"/>'
        '</linearGradient></defs>',
        '<rect width="480" height="360" fill="url(#bg)"/>',
    ]
    # little stars in the side panel
    for i in range(18):
        sx = 10 + (i * 53) % 110
        sy = 75 + (i * 97) % 280
        parts.append(f'<circle cx="{sx}" cy="{sy}" r="{1 + i % 2}" fill="#FFFFFF" fill-opacity="0.35"/>')
    sy_target = 180 - TARGET_Y
    parts.append(f'<rect x="120" y="{sy_target - 44}" width="360" height="88" fill="#FFFFFF" fill-opacity="0.06"/>')
    for _, colour, angle, x in LANES:
        cx = 240 + x
        parts.append(f'<rect x="{cx - 39}" y="0" width="78" height="360" rx="10" fill="{colour}" fill-opacity="0.10"/>')
        parts.append(f'<g transform="translate({cx - 36} {sy_target - 36}) rotate({angle} 36 36)">'
                     f'<path d="{ARROW}" fill="none" stroke="{colour}" stroke-width="5" '
                     f'stroke-linejoin="round"/></g>')
    for i, (line, colour) in enumerate(title_lines):
        d = text_path(line, 21, 60, 142 + i * 28)
        parts.append(f'<path d="{d}" fill="{colour}"/>')
    return svg(480, 360, "".join(parts))


def drum_icon():
    return svg(96, 96, """
<line x1="16" y1="8" x2="40" y2="34" stroke="#E8C9A0" stroke-width="5" stroke-linecap="round"/>
<line x1="80" y1="8" x2="56" y2="34" stroke="#E8C9A0" stroke-width="5" stroke-linecap="round"/>
<path d="M12 40 L12 72 Q48 92 84 72 L84 40 Z" fill="#FF4FA3" stroke="#FFFFFF" stroke-width="3"/>
<path d="M12 46 L30 78 L48 50 L66 80 L84 46" fill="none" stroke="#FFC93C" stroke-width="3" stroke-linejoin="round"/>
<ellipse cx="48" cy="40" rx="36" ry="12" fill="#F4F0FF" stroke="#FFFFFF" stroke-width="3"/>
""".strip())


def keyboard_icon():
    keys = "".join(f'<rect x="{8 + i * 16}" y="44" width="16" height="44" fill="#FFFFFF" stroke="#1B1035" stroke-width="2"/>'
                   for i in range(5))
    blacks = "".join(f'<rect x="{19 + i * 16}" y="44" width="10" height="26" fill="#1B1035"/>' for i in (0, 1, 3))
    note = ('<ellipse cx="62" cy="30" rx="9" ry="7" fill="#FFC93C" transform="rotate(-20 62 30)"/>'
            '<path d="M70 28 L70 4 L86 10" fill="none" stroke="#FFC93C" stroke-width="4" stroke-linecap="round"/>')
    return svg(96, 96, keys + blacks + note)


def main():
    for project, title, icon in [
        ("drum-game", [("DRUM", "#FFFFFF"), ("GAME", "#00B4A6")], drum_icon()),
        ("melody-game", [("MELODY", "#FFFFFF"), ("GAME", "#FFC93C")], keyboard_icon()),
    ]:
        write(project, "stage.svg", backdrop(title))
        write(project, "song.svg", icon)
        for name, colour, angle, _ in LANES:
            write(project, f"arrow-{name}.svg", arrow_costume(colour, angle))
            write(project, f"pad-{name}.svg", pad_costume(colour, angle, lit=False))
            write(project, f"pad-{name}-lit.svg", pad_costume(colour, angle, lit=True))
        write(project, "perfect.svg", judge_costume("PERFECT!", "#FFC93C"))
        write(project, "good.svg", judge_costume("GOOD", "#00B4A6"))
        write(project, "miss.svg", judge_costume("MISS", "#FF4FA3"))
    print("wrote assets")


if __name__ == "__main__":
    main()
