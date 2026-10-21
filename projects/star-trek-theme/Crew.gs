# Kirk, Spock, McCoy and Scotty in the transporter, from Star Trek: The Animated Series (1973).
# crew-01 to crew-12 beam them out. Go backwards (crew-12 to crew-01) to beam them in.

costumes "assets/crew-01.png", "assets/crew-02.png", "assets/crew-03.png", "assets/crew-04.png",
         "assets/crew-05.png", "assets/crew-06.png", "assets/crew-07.png", "assets/crew-08.png",
         "assets/crew-09.png", "assets/crew-10.png", "assets/crew-11.png", "assets/crew-12.png";
set_x -130;
set_y -95;

onflag {
    switch_costume "crew-01";
    set_tempo 200;
    forever {
        rest 0.5;
        play_drum 1, 0.5;  # Snare Drum
    }
}
