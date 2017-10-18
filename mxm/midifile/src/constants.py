# -*- coding: utf-8 -*-

###################################################
## Definitions of the different midi events


###################################################
## Midi channel events (The most usual events)
## also called "Channel Voice Messages" or "Voice Category messages" (ie, Status is 0x80 to 0xEF).

NOTE_OFF = 0b1000               # 0x80
# 1000cccc 0nnnnnnn 0vvvvvvv    (channel, note, velocity)

NOTE_ON =0b1001                 # 0x90
# 1001cccc 0nnnnnnn 0vvvvvvv    (channel, note, velocity)

AFTERTOUCH = 0b1010             # 0xA0 # Poly Pressure
# 1010cccc 0nnnnnnn 0vvvvvvv    (channel, note, velocity)

CONTINUOUS_CONTROLLER = 0b1011  # 0xB0 # see Channel Mode Messages!!!
# 1011cccc 0ccccccc 0vvvvvvv    (channel, controller, value)

PATCH_CHANGE = 0b1100           # 0xC0
# 1100cccc 0ppppppp             (channel, program)

CHANNEL_PRESSURE = 0b1101       # 0xD0 # Mono Pressure
# 1101cccc 0ppppppp             (channel, pressure)

PITCH_BEND = 0b1110             # 0xE0
# 1110cccc 0vvvvvvv 0wwwwwww    (channel, value-lo, value-hi)


###################################################
##  Channel Mode Messages (Continuous Controller)
##  They share a status byte.
##  The controller makes the difference here

# High resolution continuous controllers (MSB)

BANK_SELECT = 0x00
MODULATION_WHEEL = 0x01
BREATH_CONTROLLER = 0x02
FOOT_CONTROLLER = 0x04
PORTAMENTO_TIME = 0x05
DATA_ENTRY = 0x06
CHANNEL_VOLUME = 0x07
BALANCE = 0x08
PAN = 0x0A
EXPRESSION_CONTROLLER = 0x0B
EFFECT_CONTROL_1 = 0x0C
EFFECT_CONTROL_2 = 0x0D
GEN_PURPOSE_CONTROLLER_1 = 0x10
GEN_PURPOSE_CONTROLLER_2 = 0x11
GEN_PURPOSE_CONTROLLER_3 = 0x12
GEN_PURPOSE_CONTROLLER_4 = 0x13

# High resolution continuous controllers (LSB)

BANK_SELECT = 0x20
MODULATION_WHEEL = 0x21
BREATH_CONTROLLER = 0x22
FOOT_CONTROLLER = 0x24
PORTAMENTO_TIME = 0x25
DATA_ENTRY = 0x26
CHANNEL_VOLUME = 0x27
BALANCE = 0x28
PAN = 0x2A
EXPRESSION_CONTROLLER = 0x2B
EFFECT_CONTROL_1 = 0x2C
EFFECT_CONTROL_2 = 0x2D
GENERAL_PURPOSE_CONTROLLER_1 = 0x30
GENERAL_PURPOSE_CONTROLLER_2 = 0x31
GENERAL_PURPOSE_CONTROLLER_3 = 0x32
GENERAL_PURPOSE_CONTROLLER_4 = 0x33

# Switches

SUSTAIN_ONOFF = 0x40
PORTAMENTO_ONOFF = 0x41
SOSTENUTO_ONOFF = 0x42
SOFT_PEDAL_ONOFF = 0x43
LEGATO_ONOFF = 0x44
HOLD_2_ONOFF = 0x45

# Low resolution continuous controllers

SOUND_CONTROLLER_1 = 0x46                  # (TG: Sound Variation;   FX: Exciter On/Off)
SOUND_CONTROLLER_2 = 0x47                  # (TG: Harmonic Content;   FX: Compressor On/Off)
SOUND_CONTROLLER_3 = 0x48                  # (TG: Release Time;   FX: Distortion On/Off)
SOUND_CONTROLLER_4 = 0x49                  # (TG: Attack Time;   FX: EQ On/Off)
SOUND_CONTROLLER_5 = 0x4A                  # (TG: Brightness;   FX: Expander On/Off)75	SOUND_CONTROLLER_6   (TG: Undefined;   FX: Reverb OnOff)
SOUND_CONTROLLER_7 = 0x4C                  # (TG: Undefined;   FX: Delay OnOff)
SOUND_CONTROLLER_8 = 0x4D                  # (TG: Undefined;   FX: Pitch Transpose OnOff)
SOUND_CONTROLLER_9 = 0x4E                  # (TG: Undefined;   FX: Flange/Chorus OnOff)
SOUND_CONTROLLER_10 = 0x4F                 # (TG: Undefined;   FX: Special Effects OnOff)
GENERAL_PURPOSE_CONTROLLER_5 = 0x50
GENERAL_PURPOSE_CONTROLLER_6 = 0x51
GENERAL_PURPOSE_CONTROLLER_7 = 0x52
GENERAL_PURPOSE_CONTROLLER_8 = 0x53
PORTAMENTO_CONTROL = 0x54                  # (PTC)   (0vvvvvvv is the source Note number)   (Detail)
EFFECTS_1 = 0x5B                           # (Ext. Effects Depth)
EFFECTS_2 = 0x5C                           # (Tremelo Depth)
EFFECTS_3 = 0x5D                           # (Chorus Depth)
EFFECTS_4 = 0x5E                           # (Celeste Depth)
EFFECTS_5 = 0x5F                           # (Phaser Depth)
DATA_INCREMENT = 0x60                      # (0vvvvvvv is n/a; use 0)
DATA_DECREMENT = 0x61                      # (0vvvvvvv is n/a; use 0)
NON_REGISTERED_PARAMETER_NUMBER = 0x62     # (LSB)
NON_REGISTERED_PARAMETER_NUMBER = 0x63     # (MSB)
REGISTERED_PARAMETER_NUMBER = 0x64         # (LSB)
REGISTERED_PARAMETER_NUMBER = 0x65         # (MSB)

# Channel Mode messages - (Detail)

ALL_SOUND_OFF = 0x78
RESET_ALL_CONTROLLERS = 0x79
LOCAL_CONTROL_ONOFF = 0x7A
ALL_NOTES_OFF = 0x7B
OMNI_MODE_OFF = 0x7C          # (also causes ANO)
OMNI_MODE_ON = 0x7D           # (also causes ANO)
MONO_MODE_ON = 0x7E           # (Poly Off; also causes ANO)
POLY_MODE_ON = 0x7F           # (Mono Off; also causes ANO)



###################################################
## System Common Messages, for all channels

SYSTEM_EXCLUSIVE = 0xF0
# 11110000 0iiiiiii 0ddddddd ... 11110111

MTC = 0xF1 # MIDI Time Code Quarter Frame
# 11110001

SONG_POSITION_POINTER = 0xF2
# 11110010 0vvvvvvv 0wwwwwww (lo-position, hi-position)

SONG_SELECT = 0xF3
# 11110011 0sssssss (songnumber)

#UNDEFINED = 0xF4
## 11110100

#UNDEFINED = 0xF5
## 11110101

TUNING_REQUEST = 0xF6
# 11110110

END_OFF_EXCLUSIVE = 0xF7 # terminator
# 11110111 # End of system exclusive


###################################################
## Midifile meta-events

SEQUENCE_NUMBER     = 0x00      # 00 02 ss ss (seq-number)

TEXT                = 0x01      # 01 len text...
COPYRIGHT           = 0x02      # 02 len text...
SEQUENCE_NAME       = 0x03      # 03 len text...
INSTRUMENT_NAME     = 0x04      # 04 len text...
LYRIC               = 0x05      # 05 len text...
MARKER              = 0x06      # 06 len text...
CUEPOINT            = 0x07      # 07 len text...
PROGRAM_NAME        = 0x08      # 08 len text...
DEVICE_NAME         = 0x09      # 09 len text...

MIDI_CH_PREFIX      = 0x20      # MIDI channel prefix assignment (unofficial)

MIDI_PORT           = 0x21      # 21 01 port, legacy stuff but still used
END_OF_TRACK        = 0x2F      # 2f 00
TEMPO               = 0x51      # 51 03 tt tt tt (tempo in us/quarternote)
SMTP_OFFSET         = 0x54      # 54 05 hh mm ss ff xx
TIME_SIGNATURE      = 0x58      # 58 04 nn dd cc bb
KEY_SIGNATURE       = 0x59      # ??? len text...
SEQUENCER_SPECIFIC  = 0x7F      # Sequencer specific event

FILE_HEADER     = b'MThd'
TRACK_HEADER    = b'MTrk'

###################################################
## System Realtime messages
## I don't supose these are to be found in midi files?!

TIMING_CLOCK   = 0xF8
# undefined    = 0xF9
SONG_START     = 0xFA
SONG_CONTINUE  = 0xFB
SONG_STOP      = 0xFC
# undefined    = 0xFD
ACTIVE_SENSING = 0xFE
SYSTEM_RESET   = 0xFF


###################################################
## META EVENT, it is used only in midi files.
## In transmitted data it means system reset!!!

META_EVENT     = 0xFF
# 11111111


###################################################
## Helper functions

def is_status(byte):
    return (byte & 0x80) == 0x80 # 1000 0000

GM_PATCHNAMES = {
    1: 'Acoustic Grand Piano',
    2: 'Bright Acoustic Piano',
    3: 'Electric Grand Piano',
    4: 'Honky-tonk Piano',
    5: 'Electric Piano 1',
    6: 'Electric Piano 2',
    7: 'Harpsichord',
    8: 'Clavi',
    9: 'Celesta',
    10: 'Glockenspiel',
    11: 'Music Box',
    12: 'Vibraphone',
    13: 'Marimba',
    14: 'Xylophone',
    15: 'Tubular Bells',
    16: 'Dulcimer',
    17: 'Drawbar Organ',
    18: 'Percussive Organ',
    19: 'Rock Organ',
    20: 'Church Organ',
    21: 'Reed Organ',
    22: 'Accordion',
    23: 'Harmonica',
    24: 'Tango Accordion',
    25: 'Acoustic Guitar (nylon)',
    26: 'Acoustic Guitar (steel)',
    27: 'Electric Guitar (jazz)',
    28: 'Electric Guitar (clean)',
    29: 'Electric Guitar (muted)',
    30: 'Overdriven Guitar',
    31: 'Distortion Guitar',
    32: 'Guitar harmonics',
    33: 'Acoustic Bass',
    34: 'Electric Bass (finger)',
    35: 'Electric Bass (pick)',
    36: 'Fretless Bass',
    37: 'Slap Bass 1',
    38: 'Slap Bass 2',
    39: 'Synth Bass 1',
    40: 'Synth Bass 2',
    41: 'Violin',
    42: 'Viola',
    43: 'Cello',
    44: 'Contrabass',
    45: 'Tremolo Strings',
    46: 'Pizzicato Strings',
    47: 'Orchestral Harp',
    48: 'Timpani',
    49: 'String Ensemble 1',
    50: 'String Ensemble 2',
    51: 'SynthStrings 1',
    52: 'SynthStrings 2',
    53: 'Choir Aahs',
    54: 'Voice Oohs',
    55: 'Synth Voice',
    56: 'Orchestra Hit',
    57: 'Trumpet',
    58: 'Trombone',
    59: 'Tuba',
    60: 'Muted Trumpet',
    61: 'French Horn',
    62: 'Brass Section',
    63: 'SynthBrass 1',
    64: 'SynthBrass 2',
    65: 'Soprano Sax',
    66: 'Alto Sax',
    67: 'Tenor Sax',
    68: 'Baritone Sax',
    69: 'Oboe',
    70: 'English Horn',
    71: 'Bassoon',
    72: 'Clarinet',
    73: 'Piccolo',
    74: 'Flute',
    75: 'Recorder',
    76: 'Pan Flute',
    77: 'Blown Bottle',
    78: 'Shakuhachi',
    79: 'Whistle',
    80: 'Ocarina',
    81: 'Lead 1 (square)',
    82: 'Lead 2 (sawtooth)',
    83: 'Lead 3 (calliope)',
    84: 'Lead 4 (chiff)',
    85: 'Lead 5 (charang)',
    86: 'Lead 6 (voice)',
    87: 'Lead 7 (fifths)',
    88: 'Lead 8 (bass + lead)',
    89: 'Pad 1 (new age)',
    90: 'Pad 2 (warm)',
    91: 'Pad 3 (polysynth)',
    92: 'Pad 4 (choir)',
    93: 'Pad 5 (bowed)',
    94: 'Pad 6 (metallic)',
    95: 'Pad 7 (halo)',
    96: 'Pad 8 (sweep)',
    97: 'FX 1 (rain)',
    98: 'FX 2 (soundtrack)',
    99: 'FX 3 (crystal)',
    100: 'FX 4 (atmosphere)',
    101: 'FX 5 (brightness)',
    102: 'FX 6 (goblins)',
    103: 'FX 7 (echoes)',
    104: 'FX 8 (sci-fi)',
    105: 'Sitar',
    106: 'Banjo',
    107: 'Shamisen',
    108: 'Koto',
    109: 'Kalimba',
    110: 'Bag pipe',
    111: 'Fiddle',
    112: 'Shanai',
    113: 'Tinkle Bell',
    114: 'Agogo',
    115: 'Steel Drums',
    116: 'Woodblock',
    117: 'Taiko Drum',
    118: 'Melodic Tom',
    119: 'Synth Drum',
    120: 'Reverse Cymbal',
    121: 'Guitar Fret Noise',
    122: 'Breath Noise',
    123: 'Seashore',
    124: 'Bird Tweet',
    125: 'Telephone Ring',
    126: 'Helicopter',
    127: 'Applause',
    128: 'Gunshot',
}