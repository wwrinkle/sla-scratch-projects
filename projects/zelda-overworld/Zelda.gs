costumes "assets/zelda-1.svg";
set_x -150;
set_y -98;

onflag {
    switch_costume "zelda-1";
    set_tempo 150;
    beat = 1;  # a variable, so beat / 3 stays a division block in Scratch
    forever {
        play_drum 1, beat;      # Snare Drum, quarter note
        play_drum 1, beat / 3;  # eighth note triplet
        play_drum 1, beat / 3;
        play_drum 1, beat / 3;
        play_drum 1, beat;      # quarter note
        play_drum 1, beat;      # quarter note
    }
}
