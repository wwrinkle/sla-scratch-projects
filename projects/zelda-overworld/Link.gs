# Link plays the melody. Students add costume and backdrop changes
# between the notes to animate their music video.
# Sprites are from The Legend of Zelda (NES, 1986).
# Costumes: -1 and -2 walking, -3 walking sideways, -4 sword attack,
# -5 holding up the Triforce.

costumes "assets/link-1.svg", "assets/link-2.svg", "assets/link-3.svg",
         "assets/link-4.svg", "assets/link-5.svg";
set_x -60;
set_y -76;

onflag {
    switch_costume "link-1";
    switch_backdrop "field";
    set_tempo 130;
    set_instrument 20;  # Synth Lead

    # Bar 1
    play_note 70, 2;     # B♭4
    play_note 65, 1.5;   # F4
    play_note 70, 0.5;   # B♭4
    # Bar 2
    play_note 70, 0.25;  # B♭4
    play_note 72, 0.25;  # C5
    play_note 74, 0.25;  # D5
    play_note 75, 0.25;  # E♭5
    play_note 77, 2;     # F5
    play_note 77, 0.33;  # F5
    play_note 78, 0.33;  # G♭5
    play_note 80, 0.34;  # A♭5
    # Bar 3
    play_note 82, 2;     # B♭5
    play_note 82, 0.33;  # B♭5
    play_note 80, 0.33;  # A♭5
    play_note 78, 0.34;  # G♭5
    play_note 80, 0.75;  # A♭5
    play_note 78, 0.25;  # G♭5
    # Bar 4
    play_note 77, 3;     # F5
    play_note 77, 1;     # F5
    # Bar 5
    play_note 75, 0.5;   # E♭5
    play_note 75, 0.25;  # E♭5
    play_note 77, 0.25;  # F5
    play_note 78, 2;     # G♭5
    play_note 77, 0.5;   # F5
    play_note 75, 0.5;   # E♭5
    # Bar 6
    play_note 73, 0.5;   # D♭5
    play_note 73, 0.25;  # D♭5
    play_note 75, 0.25;  # E♭5
    play_note 77, 2;     # F5
    play_note 75, 0.5;   # E♭5
    play_note 73, 0.5;   # D♭5
    # Bar 7
    play_note 72, 0.5;   # C5
    play_note 72, 0.25;  # C5
    play_note 74, 0.25;  # D5
    play_note 76, 2;     # E5
    play_note 79, 1;     # G5
    # Bar 8
    play_note 77, 0.5;   # F5
    play_note 65, 0.25;  # F4
    play_note 65, 0.25;  # F4
    play_note 65, 0.5;   # F4
    play_note 65, 0.25;  # F4
    play_note 65, 0.25;  # F4
    play_note 65, 0.5;   # F4
    play_note 65, 0.25;  # F4
    play_note 65, 0.25;  # F4
    play_note 65, 0.5;   # F4
    play_note 65, 0.5;   # F4
}
