# Costumes: -1 standing, -2 arms up, -3 lunging, -4 weakened (turns brown).

costumes "assets/ganon-1.svg", "assets/ganon-2.svg", "assets/ganon-3.svg", "assets/ganon-4.svg";
set_x 150;
set_y -66;

onflag {
    switch_costume "ganon-1";
    set_tempo 150;
    set_instrument 6;  # Bass
    beat = 1;  # a variable, so beat / 3 stays a division block in Scratch
    forever {
        # bar 1
        play_note 48, beat;      # quarter note
        play_note 48, beat / 3;  # eighth note triplet
        play_note 48, beat / 3;
        play_note 46, beat / 3;
        play_note 48, beat;      # quarter note
        play_note 48, beat;      # quarter note

        # bar 2
        play_note 46, beat;      # quarter note
        play_note 46, beat / 3;  # eighth note triplet
        play_note 46, beat / 3;
        play_note 44, beat / 3;
        play_note 46, beat;      # quarter note
        play_note 46, beat;      # quarter note

        #bar 3
        play_note 44, beat;      # quarter note
        play_note 44, beat / 3;  # eighth note triplet
        play_note 44, beat / 3;
        play_note 42, beat / 3;
        play_note 44, beat;      # quarter note
        play_note 44, beat;      # quarter note

        # bar 4
        play_note 39, beat;      # quarter note
        play_note 39, beat / 3;  # eighth note triplet
        play_note 39, beat / 3;
        play_note 37, beat / 3;
        play_note 39, beat;      # quarter note
        play_note 39, beat;      # quarter note

        # bar 5
        play_note 37, beat;      # quarter note
        play_note 37, beat / 3;  # eighth note triplet
        play_note 37, beat / 3;
        play_note 35, beat / 3;
        play_note 37, beat;      # quarter note
        play_note 37, beat;      # quarter note

        # bar 6
        play_note 36, beat;      # quarter note
        play_note 36, beat / 3;  # eighth note triplet
        play_note 36, beat / 3;
        play_note 34, beat / 3;
        play_note 36, beat;      # quarter note
        play_note 36, beat;      # quarter note

        # bar 7
        play_note 38, beat;      # quarter note
        play_note 38, beat / 3;  # eighth note triplet
        play_note 38, beat / 3;
        play_note 36, beat / 3;
        play_note 38, beat;      # quarter note
        play_note 38, beat;      # quarter note

        # bar 8
        play_note 43, beat;      # quarter note
        play_note 43, beat / 3;  # eighth note triplet
        play_note 43, beat / 3;
        play_note 41, beat / 3;
        play_note 43, beat;      # quarter note
        play_note 43, beat;      # quarter note
    }
}
