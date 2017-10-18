"""
The smallest possible type 0 midi file. 1 note for 1 bar duration.
"""

from mxm.midifile import MidiOutFile
from mxm.midifile import exampledir

QUARTER = 480
BAR = QUARTER*4
NOTE = 0x3C # middle C
GRAND_PIANO = 0

# in type 0 midi files there is only one track.
# there can be different midi channels in the same track, mo matter
# the type of midi file

out_file = open(exampledir('midi-out/mxm_midifile_type_0_minimal.mid'), 'wb')
midi = MidiOutFile(out_file)
midi.header(format=0, nTracks=1, division=QUARTER)

#####################
# track 0 begin

midi.start_of_track()

midi.tempo_bpm(135)
midi.time_signature(nn=4, dd=2, cc=24, bb=8)
midi.patch_change(0, GRAND_PIANO)

# note on
midi.update_time(0)
midi.note_on(0, NOTE, 0x64)

# note off one bar later
midi.update_time(BAR)
midi.note_off(0, NOTE, 0x40)

midi.update_time(0)
midi.end_of_track()

# track 0 end
#####################
