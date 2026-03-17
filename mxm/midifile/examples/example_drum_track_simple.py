"""
Simple drum track example — no loops, no abstractions.
Each note-on and note-off is written explicitly, one line at a time.

Writes 1 bar of a standard rock beat on channel 10 (GM percussion):

    Beat:    1  .  .  .  2  .  .  .  3  .  .  .  4  .  .  .
    Hi-Hat:  x  x  x  x  x  x  x  x  x  x  x  x  x  x  x  x
    Snare:   .  .  .  .  X  .  .  .  .  .  .  .  X  .  .  .
    Kick:    X  .  .  X  .  .  X  .  X  .  .  .  .  .  X  .
"""

from mxm.midifile import MidiOutFile
from mxm.midifile import exampledir

# Timing constants
QUARTER = 480                  # ticks per quarter note
SIXTEENTH = QUARTER // 4      # ticks per 16th note (120 per 16th)

# GM Drum note numbers (channel 10 percussion map)
KICK = 36        # Bass Drum 1
SNARE = 38       # Acoustic Snare
CLOSED_HH = 42   # Closed Hi-Hat
CRASH = 49       # Crash Cymbal 1

# MIDI channel 9 = "channel 10" in musician-speak (0-indexed)
DRUM_CH = 9

# Velocities
VEL_HARD = 100    # accented hits (kick, snare)
VEL_SOFT = 60     # ghost/regular hits (hi-hat)


out_file = open(exampledir('midi-out/drum_track_simple.mid'), 'wb')
midi = MidiOutFile(out_file)
midi.header(format=1, nTracks=2, division=QUARTER)

# Track 0: tempo and time signature
midi.start_of_track()
midi.sequence_name(b'Simple Drum Track')
midi.time_signature(nn=4, dd=2, cc=24, bb=8)
midi.tempo_bpm(120)
midi.end_of_track()

# Track 1: one bar of drums, every hit written out by hand
midi.start_of_track()
midi.sequence_name(b'Drums')

# ---- Step 1: beat 1 (kick + hi-hat) ----
midi.update_time(0)
midi.note_on(DRUM_CH, KICK, VEL_HARD)
midi.update_time(0)
midi.note_on(DRUM_CH, CLOSED_HH, VEL_SOFT)
midi.update_time(SIXTEENTH)
midi.note_off(DRUM_CH, KICK, 0)
midi.update_time(0)
midi.note_off(DRUM_CH, CLOSED_HH, 0)

# ---- Step 2: 1e (hi-hat) ----
midi.update_time(0)
midi.note_on(DRUM_CH, CLOSED_HH, VEL_SOFT)
midi.update_time(SIXTEENTH)
midi.note_off(DRUM_CH, CLOSED_HH, 0)

# ---- Step 3: 1& (hi-hat) ----
midi.update_time(0)
midi.note_on(DRUM_CH, CLOSED_HH, VEL_SOFT)
midi.update_time(SIXTEENTH)
midi.note_off(DRUM_CH, CLOSED_HH, 0)

# ---- Step 4: 1a (kick + hi-hat) ----
midi.update_time(0)
midi.note_on(DRUM_CH, KICK, VEL_HARD)
midi.update_time(0)
midi.note_on(DRUM_CH, CLOSED_HH, VEL_SOFT)
midi.update_time(SIXTEENTH)
midi.note_off(DRUM_CH, KICK, 0)
midi.update_time(0)
midi.note_off(DRUM_CH, CLOSED_HH, 0)

# ---- Step 5: beat 2 (snare + hi-hat) ----
midi.update_time(0)
midi.note_on(DRUM_CH, SNARE, VEL_HARD)
midi.update_time(0)
midi.note_on(DRUM_CH, CLOSED_HH, VEL_SOFT)
midi.update_time(SIXTEENTH)
midi.note_off(DRUM_CH, SNARE, 0)
midi.update_time(0)
midi.note_off(DRUM_CH, CLOSED_HH, 0)

# ---- Step 6: 2e (hi-hat) ----
midi.update_time(0)
midi.note_on(DRUM_CH, CLOSED_HH, VEL_SOFT)
midi.update_time(SIXTEENTH)
midi.note_off(DRUM_CH, CLOSED_HH, 0)

# ---- Step 7: 2& (kick + hi-hat) ----
midi.update_time(0)
midi.note_on(DRUM_CH, KICK, VEL_HARD)
midi.update_time(0)
midi.note_on(DRUM_CH, CLOSED_HH, VEL_SOFT)
midi.update_time(SIXTEENTH)
midi.note_off(DRUM_CH, KICK, 0)
midi.update_time(0)
midi.note_off(DRUM_CH, CLOSED_HH, 0)

# ---- Step 8: 2a (hi-hat) ----
midi.update_time(0)
midi.note_on(DRUM_CH, CLOSED_HH, VEL_SOFT)
midi.update_time(SIXTEENTH)
midi.note_off(DRUM_CH, CLOSED_HH, 0)

# ---- Step 9: beat 3 (kick + hi-hat) ----
midi.update_time(0)
midi.note_on(DRUM_CH, KICK, VEL_HARD)
midi.update_time(0)
midi.note_on(DRUM_CH, CLOSED_HH, VEL_SOFT)
midi.update_time(SIXTEENTH)
midi.note_off(DRUM_CH, KICK, 0)
midi.update_time(0)
midi.note_off(DRUM_CH, CLOSED_HH, 0)

# ---- Step 10: 3e (hi-hat) ----
midi.update_time(0)
midi.note_on(DRUM_CH, CLOSED_HH, VEL_SOFT)
midi.update_time(SIXTEENTH)
midi.note_off(DRUM_CH, CLOSED_HH, 0)

# ---- Step 11: 3& (hi-hat) ----
midi.update_time(0)
midi.note_on(DRUM_CH, CLOSED_HH, VEL_SOFT)
midi.update_time(SIXTEENTH)
midi.note_off(DRUM_CH, CLOSED_HH, 0)

# ---- Step 12: 3a (hi-hat) ----
midi.update_time(0)
midi.note_on(DRUM_CH, CLOSED_HH, VEL_SOFT)
midi.update_time(SIXTEENTH)
midi.note_off(DRUM_CH, CLOSED_HH, 0)

# ---- Step 13: beat 4 (snare + hi-hat) ----
midi.update_time(0)
midi.note_on(DRUM_CH, SNARE, VEL_HARD)
midi.update_time(0)
midi.note_on(DRUM_CH, CLOSED_HH, VEL_SOFT)
midi.update_time(SIXTEENTH)
midi.note_off(DRUM_CH, SNARE, 0)
midi.update_time(0)
midi.note_off(DRUM_CH, CLOSED_HH, 0)

# ---- Step 14: 4e (hi-hat) ----
midi.update_time(0)
midi.note_on(DRUM_CH, CLOSED_HH, VEL_SOFT)
midi.update_time(SIXTEENTH)
midi.note_off(DRUM_CH, CLOSED_HH, 0)

# ---- Step 15: 4& (kick + hi-hat) ----
midi.update_time(0)
midi.note_on(DRUM_CH, KICK, VEL_HARD)
midi.update_time(0)
midi.note_on(DRUM_CH, CLOSED_HH, VEL_SOFT)
midi.update_time(SIXTEENTH)
midi.note_off(DRUM_CH, KICK, 0)
midi.update_time(0)
midi.note_off(DRUM_CH, CLOSED_HH, 0)

# ---- Step 16: 4a (hi-hat) ----
midi.update_time(0)
midi.note_on(DRUM_CH, CLOSED_HH, VEL_SOFT)
midi.update_time(SIXTEENTH)
midi.note_off(DRUM_CH, CLOSED_HH, 0)

midi.update_time(0)
midi.end_of_track()

out_file.close()
print('Written: drum_track_simple.mid')
print('1 bar of 4/4 at 120 BPM on channel 10 (GM percussion)')
