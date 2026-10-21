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
    set_tempo 150;
    set_instrument 20;  # Synth Lead
    # Melody here
}
