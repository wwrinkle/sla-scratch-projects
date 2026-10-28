# The falling arrows. Included by each starter's Arrow.gs, which defines `play_hit_sound`.
# See README.md in this folder for how the pieces fit together.

# TARGET_Y: the target line (keep in step with rhythm_game_assets.py)
# START_Y: arrows appear at the top edge
# LEAD_BEATS: an arrow falls for this many beats before it reaches the line
# PERFECT, GOOD: how many seconds early or late still count as PERFECT or GOOD
%define TARGET_Y -125
%define START_Y 180
%define LEAD_BEATS 3
%define PERFECT 0.07
%define GOOD 0.15

costumes "assets/arrow-left.svg", "assets/arrow-down.svg", "assets/arrow-up.svg", "assets/arrow-right.svg";
set_x -75;
set_y 115;

var is_clone = 0;

onflag {
    hide;
    is_clone = 0;
    set_up_sound;
}

# The Song sprite broadcasts "arrow" for every note. Only the original makes a clone;
# the clone copies lane, note, beats and arrive from it.
on "arrow" {
    if is_clone == 0 {
        lane = next_lane;
        note = next_note;
        beats = next_beats;
        fall_time = LEAD_BEATS * 60 / tempo();
        arrive = timer() + fall_time;
        is_clone = 1;
        clone;
        is_clone = 0;
    }
}

onclone {
    switch_costume lane;
    set_x -75 + (lane - 1) * 85;
    set_y START_Y;
    goto_front;
    show;
    judged = 0;
    forever {
        set_y TARGET_Y + (arrive - timer()) * (START_Y - TARGET_Y) / fall_time;
        if judged == 0 {
            if abs(press_time[lane] - arrive) < GOOD {
                hit;
            } elif timer() - arrive > GOOD {
                miss;
            }
        }
        if y_position() < -170 {
            delete_this_clone;
        }
    }
}

nowarp proc hit {
    judged = 1;
    error = abs(press_time[lane] - arrive);
    press_time[lane] = -100;  # this key press is used up
    if error < PERFECT {
        score += 100;
        judgment = "perfect";
    } else {
        score += 50;
        judgment = "good";
    }
    combo += 1;
    broadcast "judge";
    set_y TARGET_Y;
    set_size 130;
    set_brightness_effect 60;
    play_hit_sound;
    delete_this_clone;
}

proc miss {
    judged = 1;
    combo = 0;
    judgment = "miss";
    broadcast "judge";
    set_ghost_effect 60;
}
