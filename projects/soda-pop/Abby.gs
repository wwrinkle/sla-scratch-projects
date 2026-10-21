costumes "assets/abby-1.svg", "assets/abby-2.svg", "assets/abby-3.svg";
set_x -92;
set_y -80;

onflag {
    switch_costume "abby-1";
    set_tempo 120;
    forever {
        play_drum 2, 1;  # Bass Drum, quarter note
    }
}
