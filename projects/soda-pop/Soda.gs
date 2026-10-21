# Soda plays the melody. Students add costume and backdrop changes
# between the notes to animate their music video.

costumes "assets/soda-1.svg", "assets/soda-2.svg";
set_x 0;
set_y -60;

onflag {
    switch_costume "soda-1";
    switch_backdrop "concert";
    set_tempo 120;
    set_instrument 2;  # Electric Piano

    # TODO: replace the next line with the chorus melody, one note per line:
    #     play_note <MIDI number>, <beats>;
    # Use `rest <beats>;` for a rest.
    say "Melody coming soon!";
}
