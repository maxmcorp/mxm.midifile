from mxm.midifile import MidiOutFile
from mxm.midifile import MidiInFile
from mxm.midifile import exampledir

"""
An example of subclassing a midi MidiOutFile class to modify a midi file.
This takes alle the notes in a midi file and transposes them.
After which its saves them in a new file.
"""

class Transposer(MidiOutFile):

    "Transposes all notes by 24 semitones"

    def _transp(self, ch, note):
        delta = 24
        if ch != 9: # not the drums!
            if 0 <= (note+delta) <= 127: # dont transpose out of midi range
                note += delta
        return note

    def note_on(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
        note = self._transp(channel, note)
        MidiOutFile.note_on(self, channel, note, velocity, use_running_status)
        
    def note_off(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
        note = self._transp(channel, note)
        MidiOutFile.note_off(self, channel, note, velocity, use_running_status)

FNAME = 'cubase-minimal-type1'
in_file  = exampledir('midi-in/%s.mid' % FNAME)
out_file = exampledir('midi-out/%s-transposed.mid' % FNAME)

midi_out = Transposer(out_file)
midi_in = MidiInFile(midi_out, in_file)
midi_in.read()

