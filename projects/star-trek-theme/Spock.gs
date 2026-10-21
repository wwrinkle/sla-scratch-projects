# Spock giving the Vulcan salute, from Star Trek: The Animated Series (1973).
# "next costume" through spock-01 to spock-13 raises his hand: live long and prosper.

costumes "assets/spock-01.png", "assets/spock-02.png", "assets/spock-03.png", "assets/spock-04.png",
         "assets/spock-05.png", "assets/spock-06.png", "assets/spock-07.png", "assets/spock-08.png",
         "assets/spock-09.png", "assets/spock-10.png", "assets/spock-11.png", "assets/spock-12.png",
         "assets/spock-13.png";
set_x -160;
set_y 95;

onflag {
    switch_costume "spock-01";
    set_instrument 6;  # Bass

    forever {
        # Bars 1–2
        repeat 4 {
            play_note 48, 1;  # C3
            play_note 43, 1;  # G2
        }
        # Bars 3–4
        repeat 4 {
            play_note 44, 1;  # A♭2
            play_note 39, 1;  # E♭2
        }
        # Bars 5–6
        repeat 4 {
            play_note 48, 1;  # C3
            play_note 43, 1;  # G2
        }
        # Bars 7–8
        repeat 4 {
            play_note 41, 1;  # F2
            play_note 36, 1;  # C2
        }
    }
}
