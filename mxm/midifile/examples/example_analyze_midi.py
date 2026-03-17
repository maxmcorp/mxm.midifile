"""
Read any MIDI file and print a human-readable summary.
Usage: python -m mxm.midifile.examples.example_analyze_midi <file.mid>
"""

import sys
from mxm.midifile import MidiInFile
from mxm.midifile.src.midi_events import MidiEvents

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def note_name(n):
    return f'{NOTE_NAMES[n % 12]}{(n // 12) - 1}'

GM_INSTRUMENTS = {
    0: 'Acoustic Grand Piano', 4: 'Electric Piano 1', 24: 'Acoustic Guitar (nylon)',
    25: 'Acoustic Guitar (steel)', 30: 'Overdriven Guitar', 32: 'Acoustic Bass',
    33: 'Finger Bass', 40: 'Violin', 48: 'String Ensemble 1', 56: 'Trumpet',
    65: 'Alto Sax', 73: 'Flute',
}

class Analyzer(MidiEvents):
    def __init__(self):
        super().__init__()
        self.format = 0
        self.division = 0
        self.n_tracks = 0
        self.track = -1
        self.track_names = {}
        self.channels = {}  # ch -> {notes, patches, note_count}
        self.tempos = []
        self.time_sigs = []
        self.abs_time = 0

    def header(self, format=0, nTracks=1, division=96):
        self.format = format
        self.n_tracks = nTracks
        self.division = division

    def start_of_track(self, n_track=0):
        super().start_of_track(n_track)
        self.track += 1
        self.abs_time = 0

    def update_time(self, new_time=0, relative=True):
        if relative:
            self.abs_time += new_time
        else:
            self.abs_time = new_time

    def sequence_name(self, text):
        self.track_names[self.track] = text.decode('latin-1', errors='replace')

    def tempo(self, value):
        bpm = round(60_000_000 / value, 1)
        self.tempos.append(bpm)

    def time_signature(self, nn, dd, cc, bb):
        self.time_sigs.append(f'{nn}/{2**dd}')

    def patch_change(self, channel, patch, use_running_status=False):
        self.channels.setdefault(channel, {'notes': set(), 'patches': set(), 'note_count': 0})
        self.channels[channel]['patches'].add(patch)

    def note_on(self, channel=0, note=0, velocity=0, use_running_status=False):
        if velocity > 0:
            ch = self.channels.setdefault(channel, {'notes': set(), 'patches': set(), 'note_count': 0})
            ch['notes'].add(note)
            ch['note_count'] += 1

if len(sys.argv) < 2:
    print('Usage: python -m mxm.midifile.examples.example_analyze_midi <file.mid>')
    sys.exit(1)

a = Analyzer()
MidiInFile(a, sys.argv[1]).read()

print(f'File:      {sys.argv[1]}')
print(f'Format:    Type {a.format}')
print(f'Tracks:    {a.n_tracks}')
print(f'Division:  {a.division} ticks/quarter')
if len(a.tempos) <= 3:
    tempo_str = ', '.join(str(t) + ' BPM' for t in a.tempos) or 'not set'
else:
    tempo_str = f'{a.tempos[0]} BPM (initial), {len(a.tempos)} tempo changes total'
print(f'Tempo:     {tempo_str}')
print(f'Time sig:  {", ".join(a.time_sigs) or "not set"}')
print()

for trk, name in sorted(a.track_names.items()):
    print(f'  Track {trk}: {name}')
print()

for ch in sorted(a.channels):
    info = a.channels[ch]
    notes = sorted(info['notes'])
    label = 'Percussion' if ch == 9 else ', '.join(
        GM_INSTRUMENTS.get(p, f'Program {p}') for p in sorted(info['patches'])
    ) or 'No program'
    low = note_name(notes[0]) if notes else '?'
    high = note_name(notes[-1]) if notes else '?'
    print(f'  Ch {ch + 1:2d}: {label} — {info["note_count"]} notes ({low} to {high})')
