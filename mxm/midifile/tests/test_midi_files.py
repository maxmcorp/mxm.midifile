from mxm.midifile import MidiInFile, MidiOutFile, testdir
import io, glob, unittest


class TestMidiFiles(unittest.TestCase):
    
    def test_midifiles(self):
        """
        Testing that the the midi files in 'tests/midifiles' can be parsed without errors.
        """
        midi_dir = testdir() + 'midifiles/*.mid'
        for i, midi_in_filename in enumerate(glob.iglob(midi_dir, recursive=True)):
            midi_out = MidiOutFile(io.BytesIO())
            midi_in = MidiInFile(midi_out, midi_in_filename)
            midi_in.read()
            midi_out.close()
        self.assertTrue(i == 4) # there are 5 files being tested


if __name__ == '__main__':
    
    unittest.main()