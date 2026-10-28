# The targets light up while their arrow key is held. A new press writes the time into
# press_time for that lane, where the Arrow clones look for it.
# The original Pad is the left lane; it makes one clone for each of the other three.

costumes "assets/pad-left.svg", "assets/pad-down.svg", "assets/pad-up.svg", "assets/pad-right.svg";
set_x -75;
set_y -125;

list keys = ["left arrow", "down arrow", "up arrow", "right arrow"];

onflag {
    hide;
    lane = 1;
    repeat 3 {
        lane += 1;
        clone;
    }
    lane = 1;
    watch_key;
}

onclone {
    watch_key;
}

onkey "left arrow" { press 1; }
onkey "down arrow" { press 2; }
onkey "up arrow" { press 3; }
onkey "right arrow" { press 4; }

# Holding a key makes the computer repeat it, so only count a press after the key was let go.
proc press key_lane {
    if $key_lane == lane and armed == 1 {
        armed = 0;
        press_time[lane] = timer();
        show;
    }
}

nowarp proc watch_key {
    switch_costume lane;
    set_x -75 + (lane - 1) * 85;
    set_y -125;
    armed = 1;
    forever {
        if not key_pressed(keys[lane]) {
            armed = 1;
            hide;
        }
    }
}
