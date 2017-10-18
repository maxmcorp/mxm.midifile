"""
This is an example that uses the MidiToText eventhandler. When an 
event is triggered on it, it prints the event to the console.

It gets the events from the MidiInFile.

So it prints all the events from the infile to the console. great for 
debugging :-s
"""

from mxm.midifile import exampledir
from mxm.midifile import MidiInFile
from mxm.midifile import MidiToCode

# test_file = testdir('midifiles/cubase-minimal-type1.mid')
# test_file = testdir('midifiles-out/mxm_midifile_type_1_minimal.mid')

# advanced Creative Commons midi file example found at:
# http://www.piano-midi.de/bach.htm
# Copyright © 1996-2016 by Bernd Krueger

test_file = exampledir('midi-in/bach_847.mid') 
midiIn = MidiInFile(MidiToCode(), test_file)
midiIn.read()
