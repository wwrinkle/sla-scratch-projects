#!/usr/bin/env python3
"""Build every goboscript project in projects/ into <name>.sb3 at the repo root.

    python3 build.py              # all projects
    python3 build.py soda-pop     # one project

Needs goboscript on PATH (or set GOBOSCRIPT=/path/to/goboscript).

After goboscript builds a project, this script tidies it for students:
- removes the goboscript logo and TurboWarp settings comments from the Stage
- gives "play note" blocks the piano keyboard picker, like blocks dragged in by hand
- sets each costume's centre to the middle of its image
- lists the sprites in their layer order (set with `layers` in the project's goboscript.toml)
- labels custom blocks from the [labels] table in goboscript.toml, so `left_arrow` can read
  "left arrow for (1) beats" in Scratch (goboscript names can't have spaces)
"""

import json
import os
import re
import struct
import subprocess
import sys
import tempfile
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECTS = ROOT / "projects"
GOBOSCRIPT = os.environ.get("GOBOSCRIPT", "goboscript")
FIXED_TIME = (2020, 1, 1, 0, 0, 0)  # same bytes for the same project, so unchanged builds don't commit


def image_size(data, data_format):
    """Width and height of an SVG or PNG costume, or None."""
    if data_format == "png":
        return struct.unpack(">II", data[16:24])  # from the PNG's IHDR header
    head = data[:2000].decode("utf-8", "replace")
    w = re.search(r'\bwidth="([\d.]+)', head)
    h = re.search(r'\bheight="([\d.]+)', head)
    return (float(w.group(1)), float(h.group(1))) if w and h else None


def block_labels(project_dir):
    """The [labels] table from goboscript.toml: proc name -> Scratch label, with %s per input."""
    config = project_dir / "goboscript.toml"
    if not config.exists():
        return {}
    return tomllib.loads(config.read_text()).get("labels", {})


def relabel(block, labels, project_name):
    mutation = block.get("mutation")
    if not mutation or "proccode" not in mutation:
        return
    name, _, args = mutation["proccode"].partition(" ")
    if name not in labels:
        return
    label = labels[name]
    if label.count("%s") != args.count("%s"):
        sys.exit(f"{project_name}: label for {name} needs {args.count('%s')} %s, not {label.count('%s')}")
    mutation["proccode"] = label


def tidy(project, files, labels={}, project_name=""):
    for target in project["targets"]:
        if target["isStage"]:
            target["comments"] = {}

        blocks = target["blocks"]
        for block_id, block in list(blocks.items()):
            if not isinstance(block, dict):
                continue
            relabel(block, labels, project_name)
            if block.get("opcode") != "music_playNoteForBeats":
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
            if "rotationCenterX" in costume or costume["dataFormat"] not in ("svg", "png"):
                continue
            size = image_size(files[costume["md5ext"]], costume["dataFormat"])
            if size:
                costume["rotationCenterX"], costume["rotationCenterY"] = size[0] / 2, size[1] / 2

    # goboscript.toml's `layers` only sets drawing order; list the sprites in that order too.
    project["targets"].sort(key=lambda t: t["layerOrder"])


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
    tidy(project, files, block_labels(project_dir), project_dir.name)
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
        fmt = costume["dataFormat"]
        data = base64.b64encode(files[costume["md5ext"]]).decode()
        scale = costume.get("bitmapResolution", 1)  # bitmap pixels per stage pixel
        w, h = image_size(files[costume["md5ext"]], fmt)
        left, top = x - costume["rotationCenterX"] / scale, y - costume["rotationCenterY"] / scale
        mime = "image/png" if fmt == "png" else "image/svg+xml"
        return (f'<image x="{left:g}" y="{top:g}" width="{w / scale:g}" height="{h / scale:g}" '
                f'href="data:{mime};base64,{data}"/>')

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
