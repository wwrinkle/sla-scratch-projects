# The four targets. Tap one (iPad) or press its arrow key (keyboard) to play that lane.
# A new press writes the time into press_time for that lane, where the Arrow clones look for it.
# The targets sit in front of the falling arrows so a tap always lands on a target.
# The original Pad is the left lane; it makes one clone for each of the other three.
# Costumes 1-4 are lit (pressed), 5-8 are the resting targets.

costumes "assets/pad-left-lit.svg", "assets/pad-down-lit.svg", "assets/pad-up-lit.svg", "assets/pad-right-lit.svg",
         "assets/pad-left.svg", "assets/pad-down.svg", "assets/pad-up.svg", "assets/pad-right.svg";
set_x -75;
set_y -125;

list keys = ["left arrow", "down arrow", "up arrow", "right arrow"];

onflag {
    lane = 1;
    repeat 3 {
        lane += 1;
        clone;
    }
    lane = 1;
    watch;
}

onclone {
    watch;
}

# Taps (and mouse clicks) on this target.
onclick { press lane; }

onkey "left arrow" { press 1; }
onkey "down arrow" { press 2; }
onkey "up arrow" { press 3; }
onkey "right arrow" { press 4; }

# Holding a key makes the computer repeat it, so only count a press after the key
# (or finger) was let go.
proc press press_lane {
    if $press_lane == lane and armed == 1 {
        armed = 0;
        press_time[lane] = timer();
        switch_costume lane;
    }
}

nowarp proc watch {
    switch_costume lane + 4;
    set_x -75 + (lane - 1) * 85;
    set_y -125;
    show;
    armed = 1;
    forever {
        if not (key_pressed(keys[lane]) or (mouse_down() and touching_mouse_pointer())) {
            armed = 1;
            switch_costume lane + 4;
        }
    }
}
