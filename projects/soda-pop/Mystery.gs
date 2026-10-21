costumes "assets/mystery-1.svg", "assets/mystery-2.svg", "assets/mystery-3.svg";
set_x -184;
set_y -80;

onflag {
    switch_costume "mystery-1";
    set_tempo 120;
    set_instrument 21;  # Synth Pad
    forever {
        play_note 36, 1;  # whole note: 1 beat on, 3 beats rest
        rest 3;
        play_note 43, 1;  # half note: 1 beat on, 1 beat rest
        rest 1;
        play_note 41, 1;  # half note: 1 beat on, 1 beat rest
        rest 1;
    }
}
