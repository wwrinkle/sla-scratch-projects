# The students' sprite. Each arrow block sends one arrow down its lane, then waits that
# many beats before the next block. The arrows play drums when you hit them:
# left Snare, down Bass Drum, up Side Stick, right Open Hi-Hat (set in Arrow.gs).
# The blocks are defined at the bottom; students only change the green flag script.

costumes "assets/song.svg";
set_x -182;
set_y -95;

onflag {
    # Easter egg for fast finishers: leave "set tempo to (70)" at the top, wrap the arrows in a
    # forever loop, and add the Music block "change tempo by (10)" at the end of the loop,
    # so every round is faster.
    set_tempo 70;
    repeat 2 {
        left_arrow 1;
        up_arrow 1;
        down_arrow 1;
        right_arrow 1;
    }
}

nowarp proc left_arrow beats { send_arrow 1, $beats; }
nowarp proc down_arrow beats { send_arrow 2, $beats; }
nowarp proc up_arrow beats { send_arrow 3, $beats; }
nowarp proc right_arrow beats { send_arrow 4, $beats; }

nowarp proc send_arrow lane, beats {
    next_lane = $lane;
    next_beats = $beats;
    broadcast "arrow";
    rest $beats;
}
