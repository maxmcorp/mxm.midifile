"""
Multi-instrument arrangement: piano melody + bass + drums on separate channels.
4 bars of a simple C major groove at 120 BPM.
"""

from mxm.midifile import MidiOutFile
from mxm.midifile import exampledir

QUARTER = 480
EIGHTH = QUARTER // 2
SIXTEENTH = QUARTER // 4
HALF = QUARTER * 2

# GM instruments
PIANO = 0
FINGERED_BASS = 33

# Channels
PIANO_CH = 0
BASS_CH = 1
DRUM_CH = 9

# GM drum notes
KICK = 36
SNARE = 38
CLOSED_HH = 42

out_file = open(exampledir('midi-out/multi_instrument.mid'), 'wb')
midi = MidiOutFile(out_file)
midi.header(format=1, nTracks=4, division=QUARTER)

# Track 0: conductor
midi.start_of_track()
midi.sequence_name(b'Multi-Instrument Demo')
midi.time_signature(nn=4, dd=2, cc=24, bb=8)
midi.tempo_bpm(120)
midi.end_of_track()

# Track 1: piano melody (channel 0)
# Simple C major melody: C-E-G-E repeated, then C-D-E-F-G-A-G-E
melody = [
    (60, EIGHTH), (64, EIGHTH), (67, EIGHTH), (64, EIGHTH),
    (60, EIGHTH), (64, EIGHTH), (67, EIGHTH), (64, EIGHTH),
    (60, EIGHTH), (62, EIGHTH), (64, EIGHTH), (65, EIGHTH),
    (67, EIGHTH), (69, EIGHTH), (67, EIGHTH), (64, QUARTER),
]
midi.start_of_track()
midi.sequence_name(b'Piano')
midi.patch_change(PIANO_CH, PIANO)
for note, dur in melody:
    midi.update_time(0)
    midi.note_on(PIANO_CH, note, 90)
    midi.update_time(dur)
    midi.note_off(PIANO_CH, note, 0)
midi.update_time(0)
midi.end_of_track()

# Track 2: bass line (channel 1)
# Root notes following C-Am-F-G, each held for a half note
bass_notes = [36, 36, 33, 35, 36, 36, 33, 35]  # C-C-A-B, C-C-A-B (low octave)
midi.start_of_track()
midi.sequence_name(b'Bass')
midi.patch_change(BASS_CH, FINGERED_BASS)
for note in bass_notes:
    midi.update_time(0)
    midi.note_on(BASS_CH, note, 100)
    midi.update_time(HALF)
    midi.note_off(BASS_CH, note, 0)
midi.update_time(0)
midi.end_of_track()

# Track 3: drums (channel 10)
# Simple beat: kick on 1 & 3, snare on 2 & 4, hi-hat on every eighth
midi.start_of_track()
midi.sequence_name(b'Drums')
for bar in range(4):
    for beat in range(4):
        # hi-hat + kick or snare on the beat
        midi.update_time(0)
        midi.note_on(DRUM_CH, CLOSED_HH, 60)
        if beat in (0, 2):
            midi.update_time(0)
            midi.note_on(DRUM_CH, KICK, 100)
        else:
            midi.update_time(0)
            midi.note_on(DRUM_CH, SNARE, 100)
        midi.update_time(EIGHTH)
        midi.note_off(DRUM_CH, CLOSED_HH, 0)
        midi.update_time(0)
        midi.note_off(DRUM_CH, KICK if beat in (0, 2) else SNARE, 0)
        # hi-hat on the "and"
        midi.update_time(0)
        midi.note_on(DRUM_CH, CLOSED_HH, 60)
        midi.update_time(EIGHTH)
        midi.note_off(DRUM_CH, CLOSED_HH, 0)
midi.update_time(0)
midi.end_of_track()

out_file.close()
print('Written: multi_instrument.mid (piano + bass + drums, 4 bars)')
