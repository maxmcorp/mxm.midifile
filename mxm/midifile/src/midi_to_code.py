# -*- coding: utf-8 -*-

"""
This class can be used to render a midi file as python code. That is, it writes the midi file
as if it should written with mxm.midifile to be that midi file.

It makes round-robin between midi and python possible,

and it makes it easier to understand how both midi and mxm.midifile works.

>>> from mxm.midifile import MidiInFile
>>> from mxm.midifile import testdir
>>> with open('/home/maxm/instances/midienv/mxm.midifile-1.0/mxm/midifile/tests/midifiles/minimal.mid', 'rb') as f:
...     midiIn = MidiInFile(MidiToCode(), f)
...     midiIn.read()
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

from mxm.midifile.src import constants as c
from mxm.midifile.src.midi_events import MidiEvents

class MidiToCode(MidiEvents):

    """
    >>> m2c = MidiToCode()
    >>> note=64; velocity=64; ch=0;
    >>> MidiToCode().note_on(ch, note, velocity)
    midi_out.update_time(new_time=0)
    midi_out.note_on(channel=0, note=64, velocity=64)
    """

    #############################
    # channel events
    
    def _time(self):
        if not hasattr(self, '_old_time'):
            self._old_time = 0

    def _pt(self):
        "prints time"
        st = 'midi_out.update_time(new_time=%s)' % self.rel_time()
        print (st)

    def note_on(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
        """
        note on sends an event when a note is pressed down
        >>> note=40; velocity=40; ch=1;
        >>> MidiToCode().note_on(ch, note, velocity)
        midi_out.update_time(new_time=0)
        midi_out.note_on(channel=1, note=40, velocity=40)
        """
        self._pt()
        if use_running_status:
            fmt_st = "midi_out.note_on(channel=%s, note=%s, velocity=%s, use_running_status=True)"
        else:
            fmt_st = "midi_out.note_on(channel=%s, note=%s, velocity=%s)"
        st = (fmt_st % (channel, note, velocity))
        if velocity == 0:
            print ( (st + ' # note off') )
        else:
            print (st)

    def note_off(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
        """
        note off sends an event when a note is released
        >>> note=40; velocity=40; ch=1;
        >>> MidiToCode().note_off(ch, note, velocity)
        midi_out.update_time(new_time=0)
        midi_out.note_off(channel=1, note=40, velocity=40)
        """
        self._pt()
        if use_running_status:
            fmt_st = "midi_out.note_off(channel=%s, note=%s, velocity=%s, use_running_status=True)"
        else:
            fmt_st = "midi_out.note_off(channel=%s, note=%s, velocity=%s)"
        st = (fmt_st % (channel, note, velocity))
        print (st)

    def aftertouch(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
        """
        >>> note=40; velocity=40; ch=1;
        >>> MidiToCode().aftertouch(ch, note, velocity)
        midi_out.update_time(new_time=0)
        midi_out.aftertouch(channel=1, note=40, velocity=40)
        """
        self._pt()
        if use_running_status:
            fmt_st = "midi_out.aftertouch(channel=%s, note=%s, velocity=%s, use_running_status=True)"
        else:
            fmt_st = "midi_out.aftertouch(channel=%s, note=%s, velocity=%s)"
        st = (fmt_st % (channel, note, velocity))
        print (st)

    def continuous_controller(self, channel, controller, value, use_running_status=False):
        """
        >>> note=40; velocity=40; ch=1;
        >>> MidiToCode().continuous_controller(ch, note, velocity)
        midi_out.update_time(new_time=0)
        midi_out.continuous_controller(channel=1, controller=40, value=40)
        """
        self._pt()
        if use_running_status:
            fmt_st = "midi_out.continuous_controller(channel=%s, controller=%s, value=%s, use_running_status=True)"
        else:
            fmt_st = "midi_out.continuous_controller(channel=%s, controller=%s, value=%s)"
        st = (fmt_st % (channel, controller, value))
        print (st)

    def patch_change(self, channel, patch, use_running_status=False):
        """
        >>> patch=40; channel=1;
        >>> MidiToCode().patch_change(channel, patch)
        midi_out.update_time(new_time=0)
        midi_out.patch_change(channel=1, patch=40) # Violin
        """
        self._pt()
        if use_running_status:
            fmt_st = "midi_out.patch_change(channel=%s, patch=%s, use_running_status=True)"
        else:
            fmt_st = 'midi_out.patch_change(channel=%s, patch=%s)'
        st = fmt_st % (channel, patch)
        print (st + ' # ' + c.GM_PATCHNAMES.get(patch+1, ''))

    def channel_pressure(self, channel, pressure, use_running_status=False):
        """
        >>> pressure=40; channel=1;
        >>> MidiToCode().channel_pressure(channel, pressure)
        midi_out.update_time(new_time=0)
        midi_out.channel_pressure(channel=1, pressure=40)
        """
        self._pt()
        if use_running_status:
            fmt_st = "midi_out.channel_pressure(channel=%s, pressure=%s, use_running_status=True)"
        else:
            fmt_st = 'midi_out.channel_pressure(channel=%s, pressure=%s)'
        st = fmt_st % (channel, pressure)
        print (st)

    def pitch_bend(self, channel, value, use_running_status=False):
        """
        note off sends an event when a note is pressed released
        >>> value=40; channel=1;
        >>> MidiToCode().pitch_bend(channel, value)
        midi_out.update_time(new_time=0)
        midi_out.pitch_bend(channel=1, value=40)
        """
        self._pt()
        if use_running_status:
            fmt_st = "midi_out.pitch_bend(channel=%s, value=%s, use_running_status=True)"
        else:
            fmt_st = 'midi_out.pitch_bend(channel=%s, value=%s)'
        st = fmt_st % (channel, value)
        print (st)



    # #####################
    # ## Common events

    # I dont believe the events commented out is used in midi files, only in realtime transmitted data.

    # def system_exclusive(self, data):
    #     """
    #     >>> MidiToCode().system_exclusive(b'abc')
    #     midi_out.update_time(new_time=0)
    #     midi_out.system_exclusive(data=[97, 98, 99])
    #     """
    #     self._pt()
    #     fmt_st = 'midi_out.system_exclusive(data=%s)'
    #     st = fmt_st % list(data)
    #     print (st)

    # def song_position_pointer(self, value):
    #     """
    #     >>> MidiToCode().song_position_pointer(b'abc')
    #     midi_out.update_time(new_time=0)
    #     midi_out.system_exclusive(data=[97, 98, 99])
    #     """
    #     self._pt()
    #     fmt_st = 'midi_out.song_position_pointer(value=%s)'
    #     st = fmt_st % value
    #     print (st)

    # def song_select(self, songNumber):
    #     self._pt()
    #     st = 'song_select: %s' % songNumber
    #     print (st)

    # def tuning_request(self):
    #     self._pt()
    #     st = 'tuning_request'
    #     print (st)

    # def midi_time_code(self, msg_type, values):
    #     self._pt()
    #     st = 'midi_time_code - msg_type: %s, values: %s' % (msg_type, values)
    #     print (st)



    # #########################

    def header(self, format=0, nTracks=1, division=96):
        """
        >>> MidiToCode().header(format=0, nTracks=1, division=96)
        from mxm.midifile import MidiOutFile
        <BLANKLINE>
        midi_out = MidiOutFile('file.mid')
        midi_out.header(format=0, nTracks=1, division=96)
        <BLANKLINE>
        """
        print ('from mxm.midifile import MidiOutFile')
        print()
        print ("midi_out = MidiOutFile('file.mid')")
        fmt_st = 'midi_out.header(format=%s, nTracks=%s, division=%s)'
        st = fmt_st % (format, nTracks, division)
        print (st)
        print()

    # def eof(self):
    #     print ('End of file' )

    def start_of_track(self, n_track=0):
        """
        >>> MidiToCode().start_of_track(n_track=0)
        midi_out.start_of_track(n_track=0)
        """
        super().start_of_track(n_track=n_track)
        fmt_st = 'midi_out.start_of_track(n_track=%s)'
        st = fmt_st % n_track
        print (st)

    def end_of_track(self):
        """
        >>> MidiToCode().end_of_track()
        midi_out.end_of_track()
        <BLANKLINE>
        <BLANKLINE>
        """
        super().end_of_track()
        print ('midi_out.end_of_track()')
        print ( '' )
        print ( '' )


    # ###############
    # # sysex event

    def sysex_event(self, data):
        """
        >>> MidiToCode().sysex_event(data=[0,2,42,255])
        midi_out.update_time(new_time=0)
        midi_out.sysex_event(data=[0, 2, 42, 255])
        """
        self._pt()
        fmt_st = 'midi_out.sysex_event(data=%s)'
        st = fmt_st % (list(data))
        print ( st )


    # #####################
    # ## meta events

    def meta_event(self, meta_type, data):
        """
        undefined meta event.
        >>> MidiToCode().meta_event(meta_type=0x10, data=[42])
        midi_out.update_time(new_time=0)
        midi_out.meta_event(meta_type=16, data=[42])
        """
        self._pt()
        fmt_st = 'midi_out.meta_event(meta_type=%s, data=%s)'
        st = fmt_st % (meta_type, list(data))
        print ( st )

    def sequence_number(self, value):
        """
        >>> MidiToCode().sequence_number(value=42)
        midi_out.update_time(new_time=0)
        midi_out.sequence_number(value=42)
        """
        self._pt()
        fmt_st = 'midi_out.sequence_number(value=%s)'
        st = fmt_st % value
        print ( st )

    def _text(self, text, methodname):
        self._pt()
        try:
            print ( 'midi_out.%s(text=%s)' % (methodname, bytes(text)) )
        except:
            print ('# iso-8859-15: %s' % text.decode('iso-8859-15', 'replace'))
            print ( 'midi_out.%s(text=%s)' % (methodname, list(text)) )

    def text(self, text):
        """
        encoding can be specific to a midi file. Only limit is 8 bytes.
        Usually it is ascii, so I show iso-8859-15 as a comment. Which is
        ascii with western european characters.
        >>> MidiToCode().text(bytes('pæleo', 'latin-1'))
        midi_out.update_time(new_time=0)
        midi_out.text(text=b'p\xe6leo')
        """
        self._text(text, 'text')

    def copyright(self, text):
        self._text(text, 'copyright')

    def sequence_name(self, text):
        self._text(text, 'sequence_name')

    def instrument_name(self, text):
        self._text(text, 'instrument_name')

    def lyric(self, text):
        self._text(text, 'lyric')

    def marker(self, text):
        self._text(text, 'marker')

    def cuepoint(self, text):
        self._text(text, 'cuepoint')

    def device_name(self, text):
        self._text(text, 'device_name')

    def midi_ch_prefix(self, channel):
        """
        >>> MidiToCode().midi_ch_prefix(channel=0b1111)
        midi_out.update_time(new_time=0)
        midi_out.midi_ch_prefix(channel=15)
        """
        self._pt()
        fmt_st = 'midi_out.midi_ch_prefix(channel=%s)'
        st = fmt_st % channel
        print ( st )

    def midi_port(self, value):
        """
        >>> MidiToCode().midi_port(value=0b1111)
        midi_out.update_time(new_time=0)
        midi_out.midi_port(value=15)
        """
        self._pt()
        fmt_st = 'midi_out.midi_port(value=%s)'
        st = fmt_st % value
        print ( st )

    def tempo(self, value):
        """
        >>> MidiToCode().tempo(value=500000)
        midi_out.update_time(new_time=0)
        midi_out.tempo(value=500000) # bpm: ~120.00
        """
        self._pt()
        bpm = (60000000.00 / value)
        fmt_st = 'midi_out.tempo(value=%s) # bpm: ~%0.2f'
        st = fmt_st % (value, bpm)
        print ( st )

    def smtp_offset(self, hour, minute, second, frame, framePart):
        """
        >>> MidiToCode().smtp_offset(hour=13, minute=37, second=0, frame=24, framePart=42)
        midi_out.update_time(new_time=0)
        midi_out.smtp_offset(hour=13, minute=37, second=0, frame=24, framePart=42)
        """
        self._pt()
        fmt_st = 'midi_out.smtp_offset(hour=%s, minute=%s, second=%s, frame=%s, framePart=%s)'
        st = fmt_st % (hour, minute, second, frame, framePart)
        print ( st )

    def time_signature(self, nn, dd, cc, bb):
        """
        >>> MidiToCode().time_signature(nn=4, dd=2, cc=96, bb=8)
        midi_out.update_time(new_time=0)
        midi_out.time_signature(nn=4, dd=2, cc=96, bb=8)
        """
        self._pt()
        fmt_st = 'midi_out.time_signature(nn=%s, dd=%s, cc=%s, bb=%s)'
        st = fmt_st % (nn, dd, cc, bb)
        print ( st )

    def key_signature(self, sf, mi):
        """
        >>> MidiToCode().key_signature(sf=7, mi=1) # Gmin
        midi_out.update_time(new_time=0)
        midi_out.key_signature(sf=7, mi=1)
        """
        self._pt()
        fmt_st = 'midi_out.key_signature(sf=%s, mi=%s)'
        st = fmt_st % (sf, mi)
        print ( st )

    def sequencer_specific(self, id, data):
        """
        >>> MidiToCode().sequencer_specific(id=[0x42], data=[0,1,2,255])
        midi_out.update_time(new_time=0)
        midi_out.sequencer_specific(id=[66], data=[0, 1, 2, 255])
        """
        self._pt()
        fmt_st = 'midi_out.sequencer_specific(id=%s, data=%s)'
        st = fmt_st % (id, list(data))
        print ( st )



if __name__ == '__main__':

    import doctest
    doctest.testmod() # run test on inline examples first

    # # https://www.reddit.com/r/WeAreTheMusicMakers/comments/3ajwe4/the_largest_midi_collection_on_the_internet/
    
    # test_file = '/home/maxm/instances/midienv/mxm.midifile-1.0/mxm/midifile/tests/midifiles/ableton-glissando.mid'
    
    # with open(test_file, 'rb') as f:
    #     # do parsing
    #     from midi_infile import MidiInFile
    #     midiIn = MidiInFile(MidiToCode(), f)
    #     midiIn.read()
