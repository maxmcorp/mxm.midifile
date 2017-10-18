"""
8 midi channels in a single track. Random 1/16 notes.
"""

from mxm.midifile import MidiOutFile
from mxm.midifile import exampledir

QUARTER = 480
BAR = QUARTER*4
SIXTENTH = int(BAR/16)
NOTE = 0x3C # middle C
GRAND_PIANO = 0

# in type 0 midi files there is only one track.
# But there can be different midi channels in the same track

# generate random notes over 4 bars. Very simple 12 tone algorithmic composition
import random
notes = []
for i in range(50):
    time = random.randint(0,(BAR*4)-SIXTENTH) # spread notes over 4 bars
    pitch = random.randint(0,127)
    channel = random.randint(0,8)
    notes.append({'type':'note_on', 'pitch':pitch, 'channel':channel, 'velocity':0x40, 'time':time})
    notes.append({'type':'note_off', 'pitch':pitch, 'channel':channel, 'velocity':0x40, 'time':time+SIXTENTH})
notes.sort(key=lambda x: x['time'])

out_file = open(exampledir('midi-out/mxm_midifile_type_0_8ch_random.mid'), 'wb')
midi = MidiOutFile(out_file)
midi.header(format=0, nTracks=1, division=QUARTER)

#####################
# track 0 begin

midi.start_of_track()

midi.tempo_bpm(135)
midi.time_signature(nn=4, dd=2, cc=24, bb=8)
for ch in range(8):
    midi.patch_change(ch, GRAND_PIANO)

for note in notes:
    midi.update_time(note['time'], relative=False)
    if note['type'] == 'note_on':
        midi.note_on(note['channel'], note['pitch'], note['velocity'])
    else:
        midi.note_off(note['channel'], note['pitch'], note['velocity'])

midi.update_time(0)
midi.end_of_track()

# track 0 end
#####################
