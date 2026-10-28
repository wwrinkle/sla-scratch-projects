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
3. **Pads** listen for the arrow keys. A key press lights the target and writes the time into
   `press_time` for that lane. Holding a key down only counts once.
4. Each Arrow clone compares the latest press in its lane with `arrive`:
   within 0.07 s is PERFECT (100 points), within 0.15 s is GOOD (50), and later than that
   with no press is a MISS (the combo resets). A hit plays the clone's sound
   (`play hit sound`, defined in each starter's `Arrow.gs`).
5. **Judge** pops up the PERFECT / GOOD / MISS word.

Costumes and backdrops are drawn by `projects/rhythm_game_assets.py`.
