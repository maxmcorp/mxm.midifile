"""
8 midi channels in 8 tracks.
"""

from mxm.midifile import MidiOutFile
from mxm.midifile import exampledir
from mxm.midifile import constants as c

QUARTER = 480
BAR = QUARTER*4
SIXTENTH = int(BAR/16)
NOTE = 0x3C # middle C
GRAND_PIANO = 0

# generate random notes over in 8 tracks over 4 bars. Very simple 12 tone algorithmic composition
import random
notes = []
tracks = []
for track_n in range(8):
    notes = []
    for i in range(10):
        time = random.randint(0,(BAR*4)-SIXTENTH) # spread notes over 4 bars
        pitch = random.randint(0,127)
        notes.append({'type':'note_on', 'pitch':pitch, 'channel':track_n, 'velocity':0x40, 'time':time})
        notes.append({'type':'note_off', 'pitch':pitch, 'channel':track_n, 'velocity':0x40, 'time':time+SIXTENTH})
    notes.sort(key=lambda x: x['time'])
    tracks.append(notes)

out_file = open(exampledir('midi-out/mxm_midifile_type_1_8ch_8trk_random.mid'), 'wb')
midi = MidiOutFile(out_file)
midi.header(format=1, nTracks=9, division=QUARTER) # 8 notes tracks + 1 timing track


#####################
# track 0 begin
midi.start_of_track()
midi.sequence_name(b'Timing track')
midi.time_signature(nn=4, dd=2, cc=24, bb=8) # optional
midi.tempo_bpm(135)
midi.end_of_track()


#####################


# >>> print([c.GM_PATCHNAMES[s] for s in sounds])
# ['Acoustic Grand Piano', 'Glockenspiel', 'Drawbar Organ', 'Acoustic Guitar (nylon)', 
# 'Distortion Guitar', 'Fretless Bass', 'Pizzicato Strings', 'French Horn']

PATCHES = [1,10,17,25,31,36,46,61]

# track 1-8 begin
for i, notes in enumerate(tracks):
    midi.start_of_track()
    midi.patch_change(i, PATCHES[i])
    midi.sequence_name(b'random piano: track ' + bytes(str(i+1), 'ascii')) # tracks start at 1 not 0
    for note in notes:
        midi.update_time(note['time'], relative=False)
        if note['type'] == 'note_on':
            midi.note_on(note['channel'], note['pitch'], note['velocity'])
        else:
            midi.note_off(note['channel'], note['pitch'], note['velocity'])
    midi.update_time(0)
    midi.end_of_track()

# tracks end
#####################
