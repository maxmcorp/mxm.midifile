"""
Scale generator: writes major, minor, and pentatonic scales as MIDI.
Each scale starts on C4 (middle C), plays one octave up and back down,
then a short rest before the next scale. All on one track, sequential.
"""

from mxm.midifile import MidiOutFile
from mxm.midifile import exampledir

QUARTER = 480
EIGHTH = QUARTER // 2

# Scale intervals (semitones from root)
SCALES = {
    'Major':             [0, 2, 4, 5, 7, 9, 11, 12],
    'Natural Minor':     [0, 2, 3, 5, 7, 8, 10, 12],
    'Harmonic Minor':    [0, 2, 3, 5, 7, 8, 11, 12],
    'Major Pentatonic':  [0, 2, 4, 7, 9, 12],
    'Minor Pentatonic':  [0, 3, 5, 7, 10, 12],
    'Blues':             [0, 3, 5, 6, 7, 10, 12],
    'Dorian':            [0, 2, 3, 5, 7, 9, 10, 12],
    'Mixolydian':        [0, 2, 4, 5, 7, 9, 10, 12],
}

ROOT = 60  # C4
VEL = 90

out_file = open(exampledir('midi-out/scales.mid'), 'wb')
midi = MidiOutFile(out_file)
midi.header(format=0, nTracks=1, division=QUARTER)

midi.start_of_track()
midi.sequence_name(b'Scales from C4')
midi.time_signature(nn=4, dd=2, cc=24, bb=8)
midi.tempo_bpm(120)
midi.patch_change(0, 0)  # piano

for name, intervals in SCALES.items():
    # Mark each scale with a text event
    midi.update_time(0)
    midi.text(name.encode())

    # Up
    for semitone in intervals:
        midi.update_time(0)
        midi.note_on(0, ROOT + semitone, VEL)
        midi.update_time(EIGHTH)
        midi.note_off(0, ROOT + semitone, 0)

    # Down (skip the top note, already played)
    for semitone in reversed(intervals[:-1]):
        midi.update_time(0)
        midi.note_on(0, ROOT + semitone, VEL)
        midi.update_time(EIGHTH)
        midi.note_off(0, ROOT + semitone, 0)

    # Rest between scales
    midi.update_time(QUARTER)

midi.update_time(0)
midi.end_of_track()

out_file.close()
print(f'Written: scales.mid ({len(SCALES)} scales, sequential on one track)')
for name in SCALES:
    print(f'  - {name}')
