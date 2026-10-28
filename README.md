# Sonic Logic Academy Scratch projects

Scratch projects (`.sb3`) for Sonic Logic Academy lessons, served by GitHub Pages so the
[SLA Scratch editor](https://scratch.soniclogicacademy.com/) can open them from a link.

Pages that open the starters:

- [Pick Your Song](https://wwrinkle.github.io/sla-scratch-projects/) (`index.html`): three
  starters for the music video lesson.
- [Pick Your Game](https://wwrinkle.github.io/sla-scratch-projects/music-game/)
  (`music-game/index.html`): the Drum Game and Melody Game rhythm game starters.

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
  Link.gs       a sprite (the file name is the sprite's name): costumes and scripts
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

### Custom block labels

goboscript names can't have spaces, so a custom block shows up in Scratch as
`left_arrow beats: (1)`. To label it the way students should read it, add a `[labels]` table
to the project's `goboscript.toml`, with one `%s` for each input:

```toml
[labels]
left_arrow = "left arrow for %s beats"
```

### Rhythm games

`drum-game` and `melody-game` share their game code in `projects/rhythm-engine/` (see its
README). Students only edit the **Song** sprite. Their costumes and backdrops are drawn by
`projects/rhythm_game_assets.py` (needs `pip install -r requirements.txt` and the Bungee font).

The Star Trek star-field backdrops are generated: edit and run
`python3 projects/star-trek-theme/make_stars.py` to change them, then rebuild.

To build on your own computer, run `./install.sh` once, then `python3 build.py` (or
`python3 build.py soda-pop`). On Linux it downloads a ready-made goboscript into `~/.local/bin`,
with no sudo needed. On other systems, or with `./install.sh --from-source`, it compiles goboscript
with Rust instead, which needs (on Ubuntu) `sudo apt install build-essential pkg-config libssl-dev`.

The ready-made goboscript comes from this repo's Releases. The **Release goboscript** Action
publishes a new one whenever `GOBOSCRIPT_REV` in `.github/workflows/build.yml` changes.

## Adding a project made in Scratch

1. In Scratch, choose **File → Save to your computer**.
2. Upload the `.sb3` to this repository (use a short, lowercase, hyphenated name, e.g. `ear-exercise.sb3`).
