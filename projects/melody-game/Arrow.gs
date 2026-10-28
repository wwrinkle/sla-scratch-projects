# Each arrow plays the note the Song sprite gave it, for that many beats.

%include ../rhythm-engine/arrow

proc set_up_sound {
    set_instrument 20;  # Synth Lead. Try 1 Piano, 16 Vibraphone, 17 Music Box, 18 Steel Drum ...
}

nowarp proc play_hit_sound {
    play_note note, beats;
}
