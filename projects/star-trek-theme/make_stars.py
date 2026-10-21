#!/usr/bin/env python3
"""Generate looping 60s-film star-field backdrops (stars-1.svg .. stars-N.svg).

Forward flight: stars stream out from a vanishing point. The field is self-similar
under one loop's zoom, so frame N flows back into frame 1 without a jump.
Each frame gets its own grain, dust, gate weave and exposure flicker.

    python3 make_stars.py          # writes assets/stars-*.svg next to this script
    python3 make_stars.py OUT_DIR  # writes somewhere else

Change FRAMES, STEP (speed) or the numbers below, run it, then rebuild. If FRAMES
changes, list the new files in stage.gs. The same seed always gives the same images.
"""
import math
import random
import sys
from pathlib import Path

W, H = 480, 360
FRAMES = 4
STEP = 1.25                      # zoom per frame
LOOP = FRAMES * math.log(STEP)   # log-radius covered by one loop
CX, CY = 252, 172                # vanishing point
R_MIN, R_MAX = 3.0, 340.0
SPAN = math.log(R_MAX / R_MIN)

rng = random.Random(1966)

STAR_COLORS = ["#fff6e2", "#fff6e2", "#fff6e2", "#ffe9c4", "#e4ecff", "#ffd9b0"]

# Flying stars: one entry per "ray"; copies every LOOP along it.
flyers = [dict(u=rng.uniform(0, LOOP), a=rng.uniform(0, 2 * math.pi),
               curl=rng.uniform(-0.35, 0.35), mag=rng.uniform(0.45, 1.0),
               color=rng.choice(STAR_COLORS))
          for _ in range(20)]

# Distant stars: too far away to move.
fixed = [dict(x=rng.uniform(0, W), y=rng.uniform(0, H),
              r=rng.choice([0.9, 1.1, 1.3, 1.6]), o=rng.uniform(0.55, 1.0),
              color=rng.choice(STAR_COLORS))
         for _ in range(45)]


def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def flyer_points(frame):
    """(x, y, t, angle) for every visible copy of every flying star; t=0 far, 1 near."""
    out = []
    for s in flyers:
        u = (s["u"] + frame * math.log(STEP)) % LOOP
        while u < SPAN:
            r = R_MIN * math.exp(u)
            ang = s["a"] + s["curl"] * u
            x, y = CX + r * math.cos(ang), CY + r * math.sin(ang) * 0.92
            if -20 < x < W + 20 and -20 < y < H + 20:
                out.append((x, y, u / SPAN, ang, r, s))
            u += LOOP
    return out


def frame_svg(frame):
    fr = random.Random(500 + frame)
    wx, wy = fr.uniform(-1.6, 1.6), fr.uniform(-1.2, 1.2)  # gate weave
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    p.append(f'''<defs>
  <radialGradient id="sky" cx="0.52" cy="0.47" r="0.75">
    <stop offset="0" stop-color="#101824"/><stop offset="0.6" stop-color="#090e18"/><stop offset="1" stop-color="#05070d"/>
  </radialGradient>
  <radialGradient id="vignette" cx="0.5" cy="0.5" r="0.72">
    <stop offset="0.55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.78"/>
  </radialGradient>
  <radialGradient id="halo">
    <stop offset="0" stop-color="#ff9466" stop-opacity="1"/><stop offset="1" stop-color="#ff9466" stop-opacity="0"/>
  </radialGradient>
  <filter id="speck" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="0.5"/></filter>
  <filter id="grainLight" x="0" y="0" width="{W}" height="{H}" filterUnits="userSpaceOnUse">
    <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" seed="{11 + frame * 7}" stitchTiles="stitch"/>
    <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 0.96  0 0 0 0 0.86  2.4 0 0 0 -1.2"/>
  </filter>
  <filter id="grainDark" x="0" y="0" width="{W}" height="{H}" filterUnits="userSpaceOnUse">
    <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="2" seed="{53 + frame * 13}" stitchTiles="stitch"/>
    <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  2.2 0 0 0 -1.0"/>
  </filter>
  <filter id="mottle" x="0" y="0" width="{W}" height="{H}" filterUnits="userSpaceOnUse">
    <feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="3" seed="{frame + 3}"/>
    <feColorMatrix type="matrix" values="0 0 0 0 0.35  0 0 0 0 0.42  0 0 0 0 0.55  1.2 0 0 0 -0.45"/>
  </filter>
</defs>''')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
    # uneven film exposure / faint dust in space
    p.append(f'<rect width="{W}" height="{H}" filter="url(#mottle)" opacity="0.1"/>')

    p.append(f'<g transform="translate({wx:.1f} {wy:.1f})">')
    # distant stars
    # Stars are plain circles with no blur filter: Scratch skips filtered shapes.
    for s in fixed:
        p.append(f'<circle cx="{s["x"]:.1f}" cy="{s["y"]:.1f}" r="{s["r"]}" fill="{s["color"]}" opacity="{s["o"]:.2f}"/>')

    pts = flyer_points(frame)
    # halation: warm red glow around bright stars, the way film bleeds highlights
    for x, y, t, ang, r, s in pts:
        b = smooth((t - 0.62) / 0.3) * s["mag"]
        if b > 0.25:
            p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{6 + 7 * b:.1f}" fill="url(#halo)" opacity="{0.4 * b:.2f}"/>')
    # motion streaks for near stars
    for x, y, t, ang, r, s in pts:
        b = smooth((t - 0.6) / 0.35) * s["mag"]
        if b > 0.2:
            back = r * (1 - 1 / STEP) * 0.35
            x0, y0 = x - back * math.cos(ang), y - back * math.sin(ang) * 0.92
            p.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="{s["color"]}" '
                     f'stroke-width="{1.2 + 2.6 * b:.1f}" stroke-linecap="round" opacity="{0.4 * b:.2f}"/>')
    # star cores
    for x, y, t, ang, r, s in pts:
        o = smooth((t - 0.55) / 0.25) * (0.5 + 0.5 * s["mag"])
        size = 1.0 + 3.2 * (t ** 1.8) * s["mag"]
        if o > 0.03:
            p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size:.2f}" fill="{s["color"]}" opacity="{min(o, 1):.2f}"/>')
    p.append('</g>')

    # film grain
    p.append(f'<rect width="{W}" height="{H}" filter="url(#grainDark)" opacity="0.25"/>')
    p.append(f'<rect width="{W}" height="{H}" filter="url(#grainLight)" opacity="0.16"/>')

    # dust and hair on the print
    p.append('<g filter="url(#speck)">')
    for _ in range(fr.randint(3, 6)):
        x, y = fr.uniform(10, W - 10), fr.uniform(10, H - 10)
        rx, ry = fr.uniform(0.6, 2.2), fr.uniform(0.5, 1.6)
        col = fr.choice(["#000", "#000", "#f4ead2"])
        p.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{col}" '
                 f'opacity="{fr.uniform(0.45, 0.85):.2f}" transform="rotate({fr.uniform(0, 180):.0f} {x:.1f} {y:.1f})"/>')
    if fr.random() < 0.6:
        x, y = fr.uniform(40, W - 40), fr.uniform(40, H - 40)
        pts_h = " ".join(f"{x + fr.uniform(-14, 14):.1f},{y + fr.uniform(-14, 14):.1f}" for _ in range(3))
        p.append(f'<path d="M{x:.1f},{y:.1f} Q{pts_h.split()[0]} {pts_h.split()[1]} T{pts_h.split()[2]}" '
                 f'fill="none" stroke="#000" stroke-width="0.7" opacity="0.6"/>')
    p.append('</g>')
    # vertical scratch along the film
    if frame % 2 == 0:
        x = fr.uniform(60, W - 60)
        p.append(f'<path d="M{x:.1f},0 Q{x + fr.uniform(-4, 4):.1f},{H / 2} {x + fr.uniform(-3, 3):.1f},{H}" '
                 f'fill="none" stroke="#efe6cf" stroke-width="0.8" opacity="{fr.uniform(0.18, 0.3):.2f}"/>')

    # colour grade: lifted, warm blacks; exposure flicker; vignette
    p.append(f'<rect width="{W}" height="{H}" fill="#2a1d12" opacity="0.16"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="#fff3d6" opacity="{fr.uniform(0.0, 0.035):.3f}"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>')
    p.append('</svg>')
    return "\n".join(p) + "\n"


out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "assets"
for f in range(FRAMES):
    (out / f"stars-{f + 1}.svg").write_text(frame_svg(f))
print("wrote", FRAMES, "frames to", out)
