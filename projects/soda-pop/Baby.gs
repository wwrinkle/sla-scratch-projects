costumes "assets/baby-1.svg", "assets/baby-2.svg", "assets/baby-3.svg";
set_x 92;
set_y -80;

onflag {
    switch_costume "baby-1";
    set_tempo 120;
    forever {
        rest 1;
        play_drum 8, 1;  # Hand Clap
    }
}
