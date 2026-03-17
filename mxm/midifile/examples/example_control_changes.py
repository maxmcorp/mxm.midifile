"""
Control change example: sustain pedal, volume swell, and pan.
Plays a chord with sustain pedal, then a note with volume fade-in and panning.
"""

from mxm.midifile import MidiOutFile
from mxm.midifile import exampledir

QUARTER = 480
HALF = QUARTER * 2
BAR = QUARTER * 4

# Common CC numbers
CC_VOLUME = 7
CC_PAN = 10        # 0=left, 64=center, 127=right
CC_SUSTAIN = 64    # 0-63=off, 64-127=on

out_file = open(exampledir('midi-out/control_changes.mid'), 'wb')
midi = MidiOutFile(out_file)
midi.header(format=0, nTracks=1, division=QUARTER)

midi.start_of_track()
midi.tempo_bpm(100)
midi.patch_change(0, 0)  # piano

# ---- Part 1: Sustain pedal ----
# Press sustain pedal, play a chord, release notes, then lift pedal
# The notes ring through because the pedal is down

midi.update_time(0)
midi.continuous_controller(0, CC_SUSTAIN, 127)  # pedal down

# Play C major chord, releasing each note after a quarter
for note in [60, 64, 67]:
    midi.update_time(0)
    midi.note_on(0, note, 80)

midi.update_time(QUARTER)
for note in [60, 64, 67]:
    midi.update_time(0)
    midi.note_off(0, note, 0)

# Notes still ring for another quarter because pedal is down
midi.update_time(QUARTER)
midi.continuous_controller(0, CC_SUSTAIN, 0)  # pedal up — sound stops

# ---- Part 2: Volume swell ----
# Fade in from silence to full volume over one bar

midi.update_time(QUARTER)  # rest
midi.continuous_controller(0, CC_VOLUME, 0)  # start silent

midi.update_time(0)
midi.note_on(0, 60, 100)

step = BAR // 16
for i in range(1, 17):
    midi.update_time(step)
    midi.continuous_controller(0, CC_VOLUME, min(127, i * 8))

midi.update_time(QUARTER)
midi.note_off(0, 60, 0)

# Reset volume
midi.update_time(0)
midi.continuous_controller(0, CC_VOLUME, 127)

# ---- Part 3: Panning ----
# Play a note that moves from left to right

midi.update_time(QUARTER)  # rest
midi.continuous_controller(0, CC_PAN, 0)  # hard left

midi.update_time(0)
midi.note_on(0, 72, 90)

step = BAR // 16
for i in range(1, 17):
    midi.update_time(step)
    midi.continuous_controller(0, CC_PAN, min(127, i * 8))

midi.update_time(QUARTER)
midi.note_off(0, 72, 0)

# Reset pan to center
midi.update_time(0)
midi.continuous_controller(0, CC_PAN, 64)

midi.update_time(0)
midi.end_of_track()

out_file.close()
print('Written: control_changes.mid (sustain pedal, volume swell, panning)')
