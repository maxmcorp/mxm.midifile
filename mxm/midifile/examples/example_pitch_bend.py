"""
Pitch bend example: plays a note and bends it up a whole step, then back down.
Simulates a guitar-style bend on a single note.
"""

from mxm.midifile import MidiOutFile
from mxm.midifile import exampledir

QUARTER = 480
EIGHTH = QUARTER // 2

# Pitch bend range: 0=max down, 8192=center (no bend), 16383=max up
# Default GM bend range is +/- 2 semitones
CENTER = 8192
# To bend up 2 semitones (a whole step), go to max (16383)
MAX_UP = 16383

out_file = open(exampledir('midi-out/pitch_bend.mid'), 'wb')
midi = MidiOutFile(out_file)
midi.header(format=0, nTracks=1, division=QUARTER)

midi.start_of_track()
midi.tempo_bpm(80)
midi.patch_change(0, 25)  # steel guitar

# Start with no bend
midi.update_time(0)
midi.pitch_bend(0, CENTER)

# Play D4 — we'll bend it up to E4
midi.update_time(0)
midi.note_on(0, 62, 100)

# Gradually bend up over one beat (8 steps)
step = QUARTER // 8
bend_range = MAX_UP - CENTER
for i in range(1, 9):
    midi.update_time(step)
    midi.pitch_bend(0, CENTER + (bend_range * i // 8))

# Hold at top for a beat
midi.update_time(QUARTER)

# Bend back down over one beat
for i in range(7, -1, -1):
    midi.update_time(step)
    midi.pitch_bend(0, CENTER + (bend_range * i // 8))

# Let it ring for another beat, then release
midi.update_time(QUARTER)
midi.note_off(0, 62, 0)

midi.update_time(0)
midi.end_of_track()

out_file.close()
print('Written: pitch_bend.mid (guitar bend: D4 up to E4 and back)')
