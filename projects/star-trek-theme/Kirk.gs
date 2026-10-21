# Captain Kirk with a glowing aura, from Star Trek: The Animated Series (1973).
# "next costume" through kirk-01 to kirk-22 plays the animation.

costumes "assets/kirk-01.png", "assets/kirk-02.png", "assets/kirk-03.png", "assets/kirk-04.png",
         "assets/kirk-05.png", "assets/kirk-06.png", "assets/kirk-07.png", "assets/kirk-08.png",
         "assets/kirk-09.png", "assets/kirk-10.png", "assets/kirk-11.png", "assets/kirk-12.png",
         "assets/kirk-13.png", "assets/kirk-14.png", "assets/kirk-15.png", "assets/kirk-16.png",
         "assets/kirk-17.png", "assets/kirk-18.png", "assets/kirk-19.png", "assets/kirk-20.png",
         "assets/kirk-21.png", "assets/kirk-22.png";
set_x 150;
set_y -85;

onflag {
    switch_costume "kirk-01";
}
