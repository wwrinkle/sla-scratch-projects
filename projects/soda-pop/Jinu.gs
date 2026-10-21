# Jinu leads the song and plays the melody. Students add costume and
# backdrop changes between the notes to animate their music video.
# Every Saja Boy has three dance poses: -1 standing, -2 arms up, -3 pointing.

costumes "assets/jinu-1.svg", "assets/jinu-2.svg", "assets/jinu-3.svg";
set_x 0;
set_y -80;

onflag {
    switch_costume "jinu-1";
    switch_backdrop "sunburst";
    set_tempo 120;
    set_instrument 2;  # Electric Piano

    # TODO: replace the next line with the chorus melody, one note per line:
    #     play_note <MIDI number>, <beats>;
    # Use `rest <beats>;` for a rest.
    say "Melody coming soon!";
}
