#!/usr/bin/env python3
"""Build every goboscript project in projects/ into <name>.sb3 at the repo root.

    python3 build.py              # all projects
    python3 build.py soda-pop     # one project

Needs goboscript on PATH (or set GOBOSCRIPT=/path/to/goboscript).

After goboscript builds a project, this script tidies it for students:
- removes the goboscript logo and TurboWarp settings comments from the Stage
- gives "play note" blocks the piano keyboard picker, like blocks dragged in by hand
- sets each costume's centre to the middle of its image
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECTS = ROOT / "projects"
GOBOSCRIPT = os.environ.get("GOBOSCRIPT", "goboscript")
FIXED_TIME = (2020, 1, 1, 0, 0, 0)  # same bytes for the same project, so unchanged builds don't commit


def svg_size(data):
    head = data[:2000].decode("utf-8", "replace")
    w = re.search(r'\bwidth="([\d.]+)', head)
    h = re.search(r'\bheight="([\d.]+)', head)
    return (float(w.group(1)), float(h.group(1))) if w and h else None


def tidy(project, files):
    for target in project["targets"]:
        if target["isStage"]:
            target["comments"] = {}

        blocks = target["blocks"]
        for block_id, block in list(blocks.items()):
            if not isinstance(block, dict) or block.get("opcode") != "music_playNoteForBeats":
                continue
            note = block["inputs"].get("NOTE")
            # A typed number looks like [1, [4, 60]]; swap it for a "note" shadow block.
            if note and isinstance(note[1], list):
                shadow_id = block_id + "-note"
                blocks[shadow_id] = {
                    "opcode": "note",
                    "next": None,
                    "parent": block_id,
                    "inputs": {},
                    "fields": {"NOTE": [str(note[1][1]), None]},
                    "shadow": True,
                    "topLevel": False,
                }
                block["inputs"]["NOTE"] = [1, shadow_id]

        for costume in target["costumes"]:
            if "rotationCenterX" in costume or costume["dataFormat"] != "svg":
                continue
            size = svg_size(files[costume["md5ext"]])
            if size:
                costume["rotationCenterX"], costume["rotationCenterY"] = size[0] / 2, size[1] / 2


def build(project_dir):
    out = ROOT / f"{project_dir.name}.sb3"
    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "raw.sb3"
        result = subprocess.run([GOBOSCRIPT, "build", str(project_dir), "-o", str(raw)],
                                capture_output=True, text=True)
        log = result.stdout + result.stderr
        # goboscript can exit 0 after reporting errors, so check its output too.
        if result.returncode != 0 or re.search(r"(?m)^(\x1b\[[0-9;]*m)*error", log):
            sys.exit(f"{project_dir.name}: goboscript failed\n{log}")

        with zipfile.ZipFile(raw) as z:
            files = {name: z.read(name) for name in z.namelist()}

    project = json.loads(files["project.json"])
    tidy(project, files)
    files["project.json"] = json.dumps(project, ensure_ascii=False, separators=(",", ":")).encode()

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(files):
            info = zipfile.ZipInfo(name, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, files[name])
    write_thumbnail(project_dir.name, project, files)
    print(f"built {out.name}")


def write_thumbnail(name, project, files):
    """thumbs/<name>.svg: the first backdrop with each visible sprite in its starting costume."""
    import base64

    def image(costume, x, y):
        data = base64.b64encode(files[costume["md5ext"]]).decode()
        w, h = svg_size(files[costume["md5ext"]])
        left, top = x - costume["rotationCenterX"], y - costume["rotationCenterY"]
        return (f'<image x="{left:g}" y="{top:g}" width="{w:g}" height="{h:g}" '
                f'href="data:image/svg+xml;base64,{data}"/>')

    parts = []
    for target in sorted(project["targets"], key=lambda t: t["layerOrder"]):
        costume = target["costumes"][target.get("currentCostume", 0)]
        if target["isStage"]:
            parts.append(image(costume, 240, 180))
        elif target.get("visible", True):
            parts.append(image(costume, 240 + target.get("x", 0), 180 - target.get("y", 0)))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">'
           + "".join(parts) + "</svg>\n")
    (ROOT / "thumbs").mkdir(exist_ok=True)
    (ROOT / "thumbs" / f"{name}.svg").write_text(svg)


def main():
    names = sys.argv[1:] or sorted(p.name for p in PROJECTS.iterdir() if (p / "stage.gs").exists())
    for name in names:
        build(PROJECTS / name)


if __name__ == "__main__":
    main()
