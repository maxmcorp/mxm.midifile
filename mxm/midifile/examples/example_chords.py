"""
Generates a MIDI file with a I-V-vi-IV chord progression in C Major.
Each chord is held for a half note (2 beats), making 2 bars of 4/4 time.

Chord progression (C Major diatonic):
  I   = C Major  (C4, E4, G4)   - the tonic, home base
  V   = G Major  (G3, B3, D4)   - the dominant, creates tension
  vi  = A minor  (A3, C4, E4)   - the relative minor, adds emotion
  IV  = F Major  (F3, A3, C4)   - the subdominant, resolves back toward home

This is one of the most common progressions in pop music.
At 120 BPM with half-note chords, the whole progression lasts 4 seconds.
"""

from mxm.midifile import MidiOutFile
from mxm.midifile import exampledir

# Timing constants (in MIDI ticks)
QUARTER = 480          # ticks per quarter note (set in header division)
HALF = QUARTER * 2     # half note = 2 quarter notes

# Instrument and dynamics
GRAND_PIANO = 0
VELOCITY = 0x64        # mezzo-forte (100 out of 127)
RELEASE_VEL = 0x40     # standard note-off velocity

# MIDI note numbers for the chord tones
# Each chord is a list of 3 notes (root position triads)
CHORDS = [
    # I: C Major — C4(60), E4(64), G4(67)
    [60, 64, 67],

    # V: G Major — G3(55), B3(59), D4(62)
    [55, 59, 62],

    # vi: A minor — A3(57), C4(60), E4(64)
    [57, 60, 64],

    # IV: F Major — F3(53), A3(57), C4(60)
    [53, 57, 60],
]

CHORD_NAMES = ['C Major (I)', 'G Major (V)', 'A minor (vi)', 'F Major (IV)']

CH = 0  # MIDI channel 0

out_file = open(exampledir('midi-out/chords_I_V_vi_IV.mid'), 'wb')
midi = MidiOutFile(out_file)
midi.header(format=1, nTracks=2, division=QUARTER)

# Track 0: tempo and time signature (conductor track)
midi.start_of_track()
midi.sequence_name(b'I-V-vi-IV in C Major')
midi.time_signature(nn=4, dd=2, cc=24, bb=8)  # 4/4 time
midi.tempo_bpm(120)
midi.end_of_track()

# Track 1: chord progression
midi.start_of_track()
midi.sequence_name(b'Piano Chords')
midi.patch_change(CH, GRAND_PIANO)

for i, chord in enumerate(CHORDS):
    # All notes in a chord start at the same time.
    # The first note has delta=0 from the previous event (or track start).
    # Subsequent notes in the same chord also have delta=0.
    for j, note in enumerate(chord):
        midi.update_time(0)
        midi.note_on(CH, note, VELOCITY)

    # After a half note duration, release all notes in the chord.
    # The first note-off carries the full duration as its delta time.
    # The remaining note-offs happen simultaneously (delta=0).
    for j, note in enumerate(chord):
        midi.update_time(HALF if j == 0 else 0)
        midi.note_off(CH, note, RELEASE_VEL)

midi.update_time(0)
midi.end_of_track()

out_file.close()
print(f'Written: chords_I_V_vi_IV.mid')
print(f'Progression: {" -> ".join(CHORD_NAMES)}')
print(f'Duration: 2 bars of 4/4 at 120 BPM (4 seconds)')
