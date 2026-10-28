# Pops up PERFECT! / GOOD / MISS each time an arrow is hit or missed.

costumes "assets/perfect.svg", "assets/good.svg", "assets/miss.svg";
set_x 52;
set_y 40;

onflag {
    hide;
}

on "judge" {
    switch_costume judgment;
    goto_front;
    set_size 70;
    set_ghost_effect 0;
    show;
    repeat 4 {
        change_size 8;
    }
    wait 0.3;
    repeat 5 {
        change_ghost_effect 20;
    }
    hide;
}
