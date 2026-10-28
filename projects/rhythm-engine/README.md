# Rhythm game engine

Shared code for the two rhythm game starters, `drum-game` and `melody-game`. Each starter
pulls these files in with `%include ../rhythm-engine/<file>`, so a fix here reaches both.
This folder has no `stage.gs`, so it isn't built as a project of its own.

How a game runs:

1. **Song** (the students' sprite) calls blocks like `left arrow for (1) beats`. Each one sets
   `next_lane` (and `next_note`, `next_beats` in the melody game), broadcasts `arrow`, then
   rests for the beats.
2. **Arrow** hears `arrow` and makes a clone. The clone falls so it reaches the target line
   exactly 3 beats later, and remembers that moment in `arrive`.
3. **Pads** are the four targets. Tapping one (iPad) or pressing its arrow key lights it and
   writes the time into `press_time` for that lane. Holding a key or finger down only counts
   once. The Pads are drawn in front of the arrows so a tap never lands on an arrow instead.
4. Each Arrow clone compares the latest press in its lane with `arrive`:
   within 0.25 s is GOOD (50 points), and within a third of that (about 0.08 s) is PERFECT
   (100). Later than that with no press is a MISS (the combo resets). The windows are set
   by `GOOD` and `PERFECT` at the top of `arrow.gs`. A hit plays the clone's sound
   (`play hit sound`, defined in each starter's `Arrow.gs`).
5. **Judge** pops up the PERFECT / GOOD / MISS word.

Costumes and backdrops are drawn by `projects/rhythm_game_assets.py`.
