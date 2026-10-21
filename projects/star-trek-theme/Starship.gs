# Starship plays the melody. Students add costume and backdrop changes
# between the notes to animate their music video.

costumes "assets/ship-1.svg", "assets/ship-2.svg";
set_x 0;
set_y 0;

onflag {
    switch_costume "ship-1";
    switch_backdrop "space";
    set_tempo 100;
    set_instrument 15;  # Choir

    # TODO: replace the next line with the theme's melody, one note per line:
    #     play_note <MIDI number>, <beats>;
    # Use `rest <beats>;` for a rest.
    say "Melody coming soon!";
}
