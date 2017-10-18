from mxm.midifile import MidiToCode

"""
This is an example that uses the MidiToText eventhandler. When an 
event is triggered on it, it prints the event to the console.

See in "example_print_file.py" how this module can generate python 
code from a midi file.
"""

midi = MidiToCode()

# non optional midi framework
midi.header(format=0, nTracks=1, division=96)
midi.start_of_track() 
midi.tempo_bpm(95)

# note on
midi.update_time(0)
midi.note_on(channel=0, note=0x40)

# note off 1 bare later
midi.update_time(96*4) # 1 bar
midi.note_off(channel=0, note=0x40)

# non optional midi framework
midi.update_time(0)
midi.end_of_track() # not optional!
