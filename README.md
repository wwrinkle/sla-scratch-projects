# Sonic Logic Academy Scratch projects

Scratch projects (`.sb3`) for Sonic Logic Academy lessons, served by GitHub Pages so the
[SLA Scratch editor](https://scratch.soniclogicacademy.com/) can open them from a link.

The [home page](https://wwrinkle.github.io/sla-scratch-projects/) (`index.html`) is the
**Pick Your Song** page: three starter projects for the music video lesson.

## Linking to a project

```
https://scratch.soniclogicacademy.com/?project_url=https://wwrinkle.github.io/sla-scratch-projects/ear-exercise.sb3
```

The editor names the project after the file. Replacing a file keeps every existing link working.

## Projects written as text (goboscript)

The starters in `projects/` are written in [goboscript](https://aspiz.uk/goboscript/docs),
a text language that compiles to Scratch. Each folder is one project:

```
projects/zelda-overworld/
  stage.gs      backdrops
  Hero.gs       a sprite (the file name is the sprite's name): costumes and scripts
  assets/       costume and backdrop images (SVG)
```

Edit a `.gs` file and push. A GitHub Action builds `<folder>.sb3` and `thumbs/<folder>.svg`
at the top of the repo and commits them, and the links pick up the new version a minute later.
Check the **Actions** tab if a change doesn't show up: a goboscript mistake fails the build there.

Melodies are written one note per line, the same as the Scratch block:

```
set_tempo 130;
set_instrument 20;   # Synth Lead
play_note 70, 2;     # play note (70) for (2) beats
rest 1;              # rest for (1) beats
```

Comments (`# …`) are for teachers. They don't appear in Scratch.

The Star Trek star-field backdrops are generated: edit and run
`python3 projects/star-trek-theme/make_stars.py` to change them, then rebuild.

To build on your own computer, install goboscript from the commit pinned in
`.github/workflows/build.yml`, then run `python3 build.py` (or `python3 build.py soda-pop`).

## Adding a project made in Scratch

1. In Scratch, choose **File → Save to your computer**.
2. Upload the `.sb3` to this repository (use a short, lowercase, hyphenated name, e.g. `ear-exercise.sb3`).
