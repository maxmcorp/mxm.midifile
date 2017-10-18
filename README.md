mxm.midifile is a python package for reading, writing and manipulating midi files
=================================================================================

I have made mxm.midifile to make reading and writing midi files in Python as pythonic, simple and straight forward as possible. It does *not* handle realtime midi data, and there are no plans to extend the code to do that. It is a complete rewrite of my older "midi" project for python 2.x.

I have tested the code on about 7000 midi files that I could find online. It is strict in the parsing and does not allow illegal values, of which there are some in midi files in the wild. It failed parsing in about 2%-3% of the files. Most of those files could not be opened in Windows media player either. The rest failed because of illegal values, like note values of 255.

I fixed all parsing errors in my code that I could find. If you find any please let me know.

Max M - maxm@mxm.dk


Installation
------------

    pip install mxm.midifile

Writing a midi file
-------------------

If you want to *write* a midi file, the simplest way to do it is:

    from mxm.midifile import MidiOutFile
    out_file = open('file-generated.mid', 'wb')
    midi = MidiOutFile(out_file)

    midi.header(format=0, nTracks=1, division=96)
    midi.start_of_track()
    
    # note on
    midi.update_time(0)
    midi.note_on(0, 0x40, 0x64)
    
    # note off one bar later
    midi.update_time(96*4)
    midi.note_off(0, 0x40, 0x40)
    
    midi.update_time(0)
    midi.end_of_track()


Reading a midi file
-------------------

If you want to *read* a midi file, the simplest way to do it is with the MidiToCode class. When MidiToCode gets a midi event from the midi parser, it prints how the event would look if it was generated with python code using mxm.midifile.

    from mxm.midifile import MidiInFile, MidiToCode
    test_file = testdir('file-generated.mid') 
    midiIn = MidiInFile(MidiToCode(), test_file)
    midiIn.read()

Which will then print:

    """
    midi = MidiOutFile('file.mid')

    midi.header(format=0, nTracks=1, division=96)
    midi.start_of_track()
    
    # note on
    midi.update_time(0)
    midi.note_on(0, 0x40, 0x64)
    
    # note off one bar later
    midi.update_time(384)
    midi.note_off(0, 0x40, 0x40)
    
    midi.update_time(0)
    midi.end_of_track()
    """

It is not very usefull in itself, but I have found that converting midi files to code like this, makes it a lot easier to understand midi files and how to use this library. It basically turns any midi track into an example. Also you can take the printed output and save it as a .py file. When you run it, it will generate a midi file

Reading, changing and saving as a new midi file
-----------------------------------------------

If you want to do something usefull, like transposing the notes in a midi file, you must subclass the "MidiOutFile" and overwrite some of the methods for your own needs.

    class Transposer(MidiOutFile):

        "Transposes all notes by 'delta' semitones"

        delta = 24

        def _transp(self, ch, note):
            if ch != 9: # not the drums!
                if 0 <= (note+self.delta) <= 127: # dont transpose out of midi range
                    note += self.
            return note

        def note_on(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
            note = self._transp(channel, note)
            MidiOutFile.note_on(self, channel, note, velocity, use_running_status)
            
        def note_off(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
            note = self._transp(channel, note)
            MidiOutFile.note_off(self, channel, note, velocity, use_running_status)

    in_file  = exampledir('file.mid')
    out_file = exampledir('file-transposed.mid')

    midi_out = Transposer(out_file)
    midi_in = MidiInFile(midi_out, in_file)
    midi_in.read()


The "MidiEvents" class in "src/midi_events.py" is the full documentation to all the methods that can be overwritten for your own classes. It is also the class you must subclass to make usefull work.

The "MidiToCode" class in "src/midi_to_code.py" is a good and simple example of how to make a complete subclass of MidiEvents for your own purpose.

mxm.midifile only reads and writes midi files. There are som rules that must be upheld when making your own midi files. mxm.midifile does not do this for you. So it is possible to make bad midi files with it. If you are in doubt it is practical to use the "MidiToCode" to analyze some good midi files and see how they do it.

If there is interest I will considder making a "SafeMidiOutFile" class that will help avoiding writing bad midi files.

Examples
--------

There are more examples in the "examples" directory.