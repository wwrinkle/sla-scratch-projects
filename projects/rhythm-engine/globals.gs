# Variables for all sprites. The Song sprite fills in next_lane / next_note / next_beats
# right before it broadcasts "arrow".

costumes "assets/stage.svg";

var next_lane = 1;
var next_note = 60;
var next_beats = 1;
var judgment = "perfect";
var score = 0;
var combo = 0;
list press_time = [-100; 4];  # when each lane's key was last pressed (timer seconds)

onflag {
    score = 0;
    combo = 0;
    show score;
    show combo;
    delete press_time;
    repeat 4 {
        add -100 to press_time;
    }
}
