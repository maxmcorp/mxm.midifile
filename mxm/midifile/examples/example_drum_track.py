"""
Generates a MIDI drum track example.

In General MIDI, channel 10 (index 9) is reserved for percussion.
Each note number maps to a specific drum sound — there is no pitch,
just different instruments. This example writes a standard rock beat

The pattern per bar (4/4 time, 16th-note grid):

    Beat:    1  .  .  .  2  .  .  .  3  .  .  .  4  .  .  .
    Hi-Hat:  x  x  x  x  x  x  x  x  x  x  x  x  x  x  x  x
    Snare:   .  .  .  .  X  .  .  .  .  .  .  .  X  .  .  .
    Kick:    X  .  .  X  .  .  X  .  X  .  .  .  .  .  X  .

    x = hit, X = accented hit, . = rest

This is repeated for 4 bars at 120 BPM.

GM Drum Map (selected):
    35 = Acoustic Bass Drum    42 = Closed Hi-Hat
    36 = Bass Drum 1           44 = Pedal Hi-Hat
    38 = Acoustic Snare        46 = Open Hi-Hat
    40 = Electric Snare        49 = Crash Cymbal 1
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

# The drum pattern for one bar, on a 16th-note grid.
# Each step is a list of (note, velocity) pairs.
# 16 steps = 16 sixteenth notes = 1 bar of 4/4.
#
#   - Hi-hat on every 16th note
#   - Kick on beats 1, the "and" of 1, the "and" of 2, beat 3
#   - Snare on beats 2 and 4
PATTERN = [
    # Beat 1 (steps 0-3)
    [(CLOSED_HH, VEL_SOFT), (KICK, VEL_HARD)],   # 1
    [(CLOSED_HH, VEL_SOFT)],                       # 1e
    [(CLOSED_HH, VEL_SOFT)],                       # 1&
    [(CLOSED_HH, VEL_SOFT), (KICK, VEL_HARD)],    # 1a

    # Beat 2 (steps 4-7)
    [(CLOSED_HH, VEL_SOFT), (SNARE, VEL_HARD)],   # 2
    [(CLOSED_HH, VEL_SOFT)],                       # 2e
    [(CLOSED_HH, VEL_SOFT), (KICK, VEL_HARD)],    # 2&
    [(CLOSED_HH, VEL_SOFT)],                       # 2a

    # Beat 3 (steps 8-11)
    [(CLOSED_HH, VEL_SOFT), (KICK, VEL_HARD)],    # 3
    [(CLOSED_HH, VEL_SOFT)],                       # 3e
    [(CLOSED_HH, VEL_SOFT)],                       # 3&
    [(CLOSED_HH, VEL_SOFT)],                       # 3a

    # Beat 4 (steps 12-15)
    [(CLOSED_HH, VEL_SOFT), (SNARE, VEL_HARD)],   # 4
    [(CLOSED_HH, VEL_SOFT)],                       # 4e
    [(CLOSED_HH, VEL_SOFT), (KICK, VEL_HARD)],    # 4&
    [(CLOSED_HH, VEL_SOFT)],                       # 4a
]

NUM_BARS = 4

out_file = open(exampledir('midi-out/drum_track.mid'), 'wb')
midi = MidiOutFile(out_file)
midi.header(format=1, nTracks=2, division=QUARTER)

# Track 0: conductor track (tempo + time signature)
midi.start_of_track()
midi.sequence_name(b'Drum Track Example')
midi.time_signature(nn=4, dd=2, cc=24, bb=8)  # 4/4 time
midi.tempo_bpm(120)
midi.end_of_track()

# Track 1: drum pattern on channel 10 (index 9)
midi.start_of_track()
midi.sequence_name(b'Drums')

# Optional: crash cymbal on beat 1 of bar 1 for a realistic start
midi.update_time(0)
midi.note_on(DRUM_CH, CRASH, VEL_HARD)
midi.update_time(SIXTEENTH)
midi.note_off(DRUM_CH, CRASH, 0)

for bar in range(NUM_BARS):
    for step, hits in enumerate(PATTERN):
        # Skip the very first step of bar 0 — we already placed the crash there.
        # The crash occupies the same time slot as step 0 of bar 0.
        if bar == 0 and step == 0:
            # Place the step-0 hits simultaneously with the crash (delta=0)
            for note, vel in hits:
                midi.update_time(0)
                midi.note_on(DRUM_CH, note, vel)
            # Note-offs after one 16th note
            for i, (note, vel) in enumerate(hits):
                midi.update_time(SIXTEENTH if i == 0 else 0)
                midi.note_off(DRUM_CH, note, 0)
            continue

        # All hits in a step sound simultaneously (delta=0 between them)
        for note, vel in hits:
            midi.update_time(0)
            midi.note_on(DRUM_CH, note, vel)

        # Release all hits after one 16th note
        for i, (note, vel) in enumerate(hits):
            midi.update_time(SIXTEENTH if i == 0 else 0)
            midi.note_off(DRUM_CH, note, 0)

midi.update_time(0)
midi.end_of_track()

out_file.close()
print(f'Written: drum_track.mid')
print(f'{NUM_BARS} bars of 4/4 at 120 BPM on channel 10 (GM percussion)')
print(f'Pattern: kick + hi-hat rock beat')
