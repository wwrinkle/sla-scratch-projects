# Costumes: -1 standing, -2 arms up, -3 lunging, -4 weakened (turns brown).

costumes "assets/ganon-1.svg", "assets/ganon-2.svg", "assets/ganon-3.svg", "assets/ganon-4.svg";
set_x 150;
set_y -66;

onflag {
    switch_costume "ganon-1";
}
