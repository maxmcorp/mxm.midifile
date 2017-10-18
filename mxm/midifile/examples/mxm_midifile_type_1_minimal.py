"""
The smallest possible complete type 1 midi file. 1 note for 1 bar duration.
"""

from mxm.midifile import MidiOutFile
from mxm.midifile import exampledir

QUARTER = 480
BAR = QUARTER*4
NOTE = 0x3C # middle C
GRAND_PIANO = 0

out_file = open(exampledir('midi-out/mxm_midifile_type_1_minimal.mid'), 'wb')
midi = MidiOutFile(out_file)
midi.header(format=1, nTracks=2, division=QUARTER)

##########################
# track 0

# in type 1 midi files first track MUST be a timing and tempo track
# and no musical events are allowed.
midi.start_of_track()
midi.sequence_name(b'Timing track')
midi.time_signature(nn=4, dd=2, cc=24, bb=8) # optional
midi.tempo_bpm(135)
midi.end_of_track()

##########################
# track 1

CH = 0
midi.start_of_track()
midi.patch_change(CH, GRAND_PIANO)
midi.sequence_name(b'piano roll %i' % CH)

midi.update_time(0)
midi.note_on(CH, NOTE, 0x64)

midi.update_time(BAR)
midi.note_off(CH, NOTE, 0x40)
midi.update_time(0)

midi.end_of_track()

