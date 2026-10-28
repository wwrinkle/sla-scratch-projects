# The students' sprite. Each arrow block sends one arrow down its lane with a note
# (MIDI number) and a length in beats, then waits that many beats before the next block.
# Hitting the arrow plays its note. Arrows here follow the melody's shape:
# the note goes up -> up arrow, down -> down arrow, stays the same -> left or right arrow.
# The blocks are defined at the bottom; students only change the green flag script.

costumes "assets/song.svg";
set_x -182;
set_y -95;

onflag {
    # Easter egg for fast finishers: leave "set tempo to (100)" at the top, wrap the arrows in a
    # forever loop, and add the Music block "change tempo by (10)" at the end of the loop,
    # so every round is faster.
    set_tempo 100;
    # Frere Jacques
    left_arrow 60, 1;   # C
    up_arrow 62, 1;     # D
    up_arrow 64, 1;     # E
    down_arrow 60, 1;   # C
    right_arrow 60, 1;  # C (same note again)
    up_arrow 62, 1;     # D
    up_arrow 64, 1;     # E
    down_arrow 60, 1;   # C
    up_arrow 64, 1;     # E
    up_arrow 65, 1;     # F
    up_arrow 67, 2;     # G
    down_arrow 64, 1;   # E
    up_arrow 65, 1;     # F
    up_arrow 67, 2;     # G
}

nowarp proc left_arrow note, beats { send_arrow 1, $note, $beats; }
nowarp proc down_arrow note, beats { send_arrow 2, $note, $beats; }
nowarp proc up_arrow note, beats { send_arrow 3, $note, $beats; }
nowarp proc right_arrow note, beats { send_arrow 4, $note, $beats; }

nowarp proc send_arrow lane, note, beats {
    next_lane = $lane;
    next_note = $note;
    next_beats = $beats;
    broadcast "arrow";
    rest $beats;
}
