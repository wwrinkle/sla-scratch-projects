# Each arrow plays one drum when it's hit. Change the numbers to change the drums:
# 1 Snare, 2 Bass Drum, 3 Side Stick, 4 Crash, 5 Open Hi-Hat, 6 Closed Hi-Hat,
# 7 Tambourine, 8 Hand Clap, 9 Claves, 10 Wood Block, 11 Cowbell, 12 Triangle ...
list drums = [1, 2, 3, 5];  # left Snare Drum, down Bass, up Side Stick, right Open Hi-Hat

%include ../rhythm-engine/arrow

proc set_up_sound {
}

nowarp proc play_hit_sound {
    play_drum drums[lane], 0.25;
}
