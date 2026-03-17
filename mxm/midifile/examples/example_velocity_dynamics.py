"""
Velocity dynamics example: a C major scale played as a crescendo then decrescendo.
Demonstrates how velocity controls volume/intensity per note.

Velocity range: 1 (pppp) to 127 (ffff)
    ~20  = pp (pianissimo)
    ~50  = mp (mezzo piano)
    ~80  = mf (mezzo forte)
    ~100 = f  (forte)
    ~127 = ff (fortissimo)
"""

from mxm.midifile import MidiOutFile
from mxm.midifile import exampledir

QUARTER = 480
EIGHTH = QUARTER // 2

# C major scale ascending and descending
SCALE_UP = [60, 62, 64, 65, 67, 69, 71, 72]       # C4 to C5
SCALE_DOWN = [72, 71, 69, 67, 65, 64, 62, 60]      # C5 to C4

# Crescendo: pp to ff
VEL_CRESC = [20, 35, 50, 65, 80, 95, 110, 127]

# Decrescendo: ff to pp
VEL_DECRESC = [127, 110, 95, 80, 65, 50, 35, 20]

out_file = open(exampledir('midi-out/velocity_dynamics.mid'), 'wb')
midi = MidiOutFile(out_file)
midi.header(format=0, nTracks=1, division=QUARTER)

midi.start_of_track()
midi.tempo_bpm(100)
midi.patch_change(0, 0)  # piano

# Ascending scale with crescendo
for note, vel in zip(SCALE_UP, VEL_CRESC):
    midi.update_time(0)
    midi.note_on(0, note, vel)
    midi.update_time(EIGHTH)
    midi.note_off(0, note, 0)

# Descending scale with decrescendo
for note, vel in zip(SCALE_DOWN, VEL_DECRESC):
    midi.update_time(0)
    midi.note_on(0, note, vel)
    midi.update_time(EIGHTH)
    midi.note_off(0, note, 0)

midi.update_time(0)
midi.end_of_track()

out_file.close()
print('Written: velocity_dynamics.mid (crescendo up, decrescendo down)')
