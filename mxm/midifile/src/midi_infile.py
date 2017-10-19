# -*- coding: utf-8 -*-

from mxm.midifile.src.raw_instream_file import RawInstreamFile
from mxm.midifile.src.midi_file_parser import MidiFileParser


class MidiInFile:

    """
    Parses a midi file, and triggers the midi events on the MidiEvents 
    object.
    
    Get example data from a minimal midi file, generated with cubase.
    >>> from mxm.midifile import testdir
    >>> test_file = testdir('midifiles/minimal.mid')
    
    Do parsing, and generate events with MidiToCode,
    so we can see what a minimal midi file contains
    >>> from mxm.midifile import MidiToCode
    >>> midi_in = MidiInFile(MidiToCode(), test_file)
    >>> midi_in.read()
    from mxm.midifile import MidiOutFile
    <BLANKLINE>
    midi_out = MidiOutFile('file.mid')
    midi_out.header(format=1, nTracks=2, division=15360)
    <BLANKLINE>
    midi_out.start_of_track(n_track=0)
    midi_out.update_time(new_time=0)
    midi_out.time_signature(nn=4, dd=2, cc=24, bb=8)
    midi_out.update_time(new_time=0)
    midi_out.tempo(value=500000) # bpm: ~120.00
    midi_out.end_of_track()
    <BLANKLINE>
    <BLANKLINE>
    midi_out.start_of_track(n_track=1)
    midi_out.update_time(new_time=0)
    midi_out.sequence_name(text=b'Synth 1')
    midi_out.update_time(new_time=0)
    midi_out.instrument_name(text=b'Synth 1')
    midi_out.update_time(new_time=0)
    midi_out.midi_port(value=4)
    midi_out.update_time(new_time=0)
    midi_out.note_on(channel=0, note=36, velocity=127)
    midi_out.update_time(new_time=61440)
    midi_out.note_off(channel=0, note=36, velocity=0)
    midi_out.end_of_track()
    <BLANKLINE>
    <BLANKLINE>
    """

    def __init__(self, event_handler, infile):
        # these could also have been mixins, would that be better? Nah!
        self.raw_in = RawInstreamFile(infile)
        self.parser = MidiFileParser(self.raw_in, event_handler)


    def read(self):
        "Start parsing the file"
        p = self.parser
        p.parseMThdChunk()
        p.parseMTrkChunks()


    def setData(self, data=''):
        "Sets the data from a plain string"
        self.raw_in.setData(data)
    
    def close(self):
        "Close the file"
        self.raw_in.close()


if __name__ == '__main__':
    
    import doctest
    doctest.testmod() # run test on inline examples first

