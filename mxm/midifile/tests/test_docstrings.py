"""
A simple way to make doctests work with unittest and "python3 setup.py test"
"""

import doctest, unittest

import mxm.midifile.src.constants as constants
import mxm.midifile.src.data_type_converters as data_type_converters
import mxm.midifile.src.event_dispatcher as event_dispatcher
import mxm.midifile.src.midi_events as midi_events
import mxm.midifile.src.midi_file_parser as midi_file_parser
import mxm.midifile.src.midi_infile as midi_infile
import mxm.midifile.src.midi_outfile as midi_outfile
import mxm.midifile.src.midi_to_code as midi_to_code
import mxm.midifile.src.raw_instream_file as raw_instream_file
import mxm.midifile.src.raw_outstream_file as raw_outstream_file

testSuite = unittest.TestSuite()

testSuite.addTest(doctest.DocTestSuite(constants))
testSuite.addTest(doctest.DocTestSuite(data_type_converters))
testSuite.addTest(doctest.DocTestSuite(event_dispatcher))
testSuite.addTest(doctest.DocTestSuite(midi_events))
testSuite.addTest(doctest.DocTestSuite(midi_file_parser))
testSuite.addTest(doctest.DocTestSuite(midi_infile))
testSuite.addTest(doctest.DocTestSuite(midi_outfile))
testSuite.addTest(doctest.DocTestSuite(midi_to_code))
testSuite.addTest(doctest.DocTestSuite(raw_instream_file))
testSuite.addTest(doctest.DocTestSuite(raw_outstream_file))

unittest.TextTestRunner(verbosity=1).run(testSuite)
