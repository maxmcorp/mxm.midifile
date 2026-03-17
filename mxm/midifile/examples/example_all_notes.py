"""
Generates a MIDI file that plays every MIDI note from 0 (C-1) to 127 (G9),
ascending one at a time. Each note is an eighth note at 120 BPM.
"""

from mxm.midifile import MidiOutFile
from mxm.midifile import exampledir

QUARTER = 480
EIGHTH = QUARTER // 2
GRAND_PIANO = 0
VELOCITY = 0x64

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def note_name(n):
    """Returns the name of a MIDI note number, e.g. 60 -> 'C4'"""
    octave = (n // 12) - 1
    return f'{NOTE_NAMES[n % 12]}{octave}'

out_file = open(exampledir('midi-out/all_notes_eighth.mid'), 'wb')
midi = MidiOutFile(out_file)
midi.header(format=1, nTracks=2, division=QUARTER)

# Track 0: tempo track
midi.start_of_track()
midi.sequence_name(b'All MIDI Notes')
midi.time_signature(nn=4, dd=2, cc=24, bb=8)
midi.tempo_bpm(120)
midi.end_of_track()

# Track 1: all 128 notes ascending
CH = 0
midi.start_of_track()
midi.sequence_name(b'Notes 0-127')
midi.patch_change(CH, GRAND_PIANO)

for note in range(128):
    midi.update_time(0)
    midi.note_on(CH, note, VELOCITY)

    midi.update_time(EIGHTH)
    midi.note_off(CH, note, 0x40)

midi.update_time(0)
midi.end_of_track()

out_file.close()
print(f'Written: all_notes_eighth.mid (128 notes, {note_name(0)} to {note_name(127)})')
