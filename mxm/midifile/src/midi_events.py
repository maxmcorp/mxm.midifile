# -*- coding: utf-8 -*-

from mxm.midifile.src import constants as c
from mxm.midifile.src.data_type_converters import manufacturer_id

class MidiEvents:

    """
    MidiEvents is the most central class in the Midi library. 
    You use it both for writing events to an output stream, 
    and as an event handler for an input stream.

    This makes it extremely easy to take input from one stream and
    send it to another. Ie. if you want to read a Midi file, do some
    processing, and send it to a midiport.

    All time values are in absolute values from the opening of a
    stream. To calculate time values, please use the MidiTime and
    MidiDeltaTime classes.
    """

    def __init__(self):
        # the time is rather global, so it needs to be stored 
        # here. Otherwise there would be no really simple way to 
        # calculate it. The alternative would be to have each event 
        # handler do it. That sucks even worse!
        self._absolute_time = 0
        self._relative_time = 0
        self._current_track = 0
        self._running_status = None

    # time handling event handlers. They should be overwritten with care

    def update_time(self, new_time=0, relative=1):
        """
        Updates the time, if relative is true, new_time is relative, 
        else it's absolute.
        >>> s = MidiEvents()
        >>> s.update_time(new_time=100)
        >>> s.rel_time(), s.abs_time()
        (100, 100)
        >>> s.update_time(new_time=100, relative=1)
        >>> s.rel_time(), s.abs_time()
        (100, 200)
        >>> s.reset_time()
        >>> s.rel_time(), s.abs_time()
        (0, 0)
        """
        if relative:
            self._relative_time = new_time
            self._absolute_time += new_time
        else:
            self._relative_time = new_time - self._absolute_time
            self._absolute_time = new_time
        assert(self._absolute_time >= 0)

    def reset_time(self):
        """
        reset time to 0
        """
        self._relative_time = 0
        self._absolute_time = 0
        
    def rel_time(self):
        "Returns the relative time"
        return self._relative_time

    def abs_time(self):
        "Returns the absolute time"
        return self._absolute_time

    # running status methods
    
    def set_running_status(self, *args):
        """
        Sets the running status. Running status is the message type and channel as a byte.
        This should be called from the individual channel messages, so something like
        'note_on' sets its own running status.
        
        Usually a channel message like 'note on' is 3 bytes:
        
          msg ch     note       velocity
        0b10010001 0b01000000 0b01000000
        
        But the first byte that contains the message type and the channel can be 
        reused so that there can be subsequent messages that just contains two bytes,
        
          note       velocity
        0b01000000 0b01000000

        Running status is used to keep track of 'msg' and 'ch' in that scenario for the 
        subsequent messages.
        So if 'ch' or 'msg' changes, the running status MUST be changed as well.
        
        >>> s = MidiEvents()

        you can either set the running status directly as a byte
        >>> channel = 0b0001
        >>> note_on_message_type = 0b1001
        >>> running_status_byte = note_on_message_type << 4 | channel
        >>> s.set_running_status(running_status_byte)
        >>> bin(s.get_running_status())
        '0b10010001'

        Or as message type and channel
        >>> s.set_running_status(0b1000, 0b0001)
        >>> bin(s.get_running_status())
        '0b10000001'

        >>> s.set_running_status(0b01111111)
        Traceback (most recent call last):
        ...
        AssertionError: Running status MUST have high bit set. It was not!
        """
        if len(args) == 2:
            run_stat = args[0]<<4|args[1]
        else:
            run_stat = args[0]
        assert(run_stat & 0b10000000), 'Running status MUST have high bit set. It was not!'
        self._running_status = run_stat

    def get_running_status(self):
        "Get the running status"
        return self._running_status

    def reset_running_status(self):
        """
        Invalidates the running status
        
        >>> s = MidiEvents()
        >>> s.set_running_status( (c.NOTE_ON<<4)+0b000 )
        >>> bin(s.get_running_status())
        '0b10010000'
        >>> s.note_off(0,64,64)
        >>> bin(s.get_running_status())
        '0b10000000'
        >>> s.reset_running_status()
        >>> repr(s.get_running_status())
        'None'
        """
        self._running_status = None


    # track handling event handlers
    
    def set_current_track(self, new_track):
        """
        Sets the current track number
        >>> s = MidiEvents()
        >>> s.set_current_track(8)
        >>> s.get_current_track()
        8
        """
        self._current_track = new_track
    
    def get_current_track(self):
        """
        Returns the current track number
        """
        return self._current_track
    
    
    #####################
    ## Midi events


    def _check_ch(self, channel):
        """
        assert 7 bit value
        >>> MidiEvents()._check_ch(15)
        >>> MidiEvents()._check_ch(16)
        Traceback (most recent call last):
        ...
        AssertionError: Illegal midi channel: 16
        """
        assert (0<=channel<=15), 'Illegal midi channel: %s' % channel


    def _check_run_stat(self, use_running_status, status):
        running_status = self.get_running_status()
        if use_running_status and ( status != running_status ):
            raise ValueError('status was: %s - running status was: %s. They MUST be the same when use_running_status==True' % (status, running_status) )
        


    ######################################
    # from here on down is the public api.

    def channel_message(self, message_type, channel, data, use_running_status=False): # msb, lsb instead of data ???
        """
        The default event handler for channel messages
        message_type: 0-15, channel: 0-15, len(bytes(data))==2
        >>> MidiEvents().channel_message(c.NOTE_ON, 0b0000, bytes([64,65]))
        >>> MidiEvents().channel_message(c.NOTE_ON, 0, bytes([64]))
        Traceback (most recent call last):
        ...
        AssertionError: Illegal data
        >>> MidiEvents().channel_message(c.NOTE_ON, 0,  bytes([64,65]), use_running_status=True)
        Traceback (most recent call last):
        ...
        ValueError: status was: 144 - running status was: None. They MUST be the same when use_running_status==True
        """
        self._check_ch(channel)
        status = (message_type<<4) + channel
        self._check_run_stat(use_running_status, status)
        assert (0<=message_type<=15), 'Illegal message type'
        assert (len(bytes(data))==2), 'Illegal data'


    def note_on(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
        """
        channel: 0-15, note: 0-127, velocity: 0-127
        >>> MidiEvents().note_on(0,64,64)
        >>> MidiEvents().note_on(64,64,64)
        Traceback (most recent call last):
        ...
        AssertionError: Illegal midi channel: 64
        """
        self._check_ch(channel)
        status = (c.NOTE_ON<<4) + channel
        self._check_run_stat(use_running_status, status)
        assert (0<=note<=127), 'Illegal note value: %s' % note
        assert (0<=velocity<=127), 'Illegal velocity value: %s' % velocity
        self.set_running_status(c.NOTE_ON, channel)


    def note_off(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
        """
        channel: 0-15, note: 0-127, velocity: 0-127
        >>> MidiEvents().note_off(0,200,64)
        Traceback (most recent call last):
        ...
        AssertionError: Illegal note value: 200
        """
        self._check_ch(channel)
        status = (c.NOTE_OFF<<4) + channel
        self._check_run_stat(use_running_status, status)
        assert (0<=note<=127), 'Illegal note value: %s' % note
        assert (0<=velocity<=127), 'Illegal velocity value: %s' % velocity
        self.set_running_status(c.NOTE_OFF, channel)


    def aftertouch(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
        #XXX should velocity not be value ???
        """
        channel: 0-15, note, velocity: 0-127
        >>> MidiEvents().aftertouch(0,64,64)
        >>> MidiEvents().aftertouch(0,64,200)
        Traceback (most recent call last):
        ...
        AssertionError: Illegal velocity value: 200
        """
        self._check_ch(channel)
        status = (c.AFTERTOUCH<<4) + channel
        self._check_run_stat(use_running_status, status)
        assert (0<=note<=127), 'Illegal note value: %s' % note
        assert (0<=velocity<=127), 'Illegal velocity value: %s' % velocity
        self.set_running_status(c.AFTERTOUCH, channel)


    def continuous_controller(self, channel, controller, value, use_running_status=False):
        """
        channel: 0-15, controller, value: 0-127
        >>> MidiEvents().continuous_controller(0,64,64)
        >>> MidiEvents().continuous_controller(0,100,300)
        Traceback (most recent call last):
        ...
        AssertionError: Illegal value: 300
        """
        self._check_ch(channel)
        status = (c.CONTINUOUS_CONTROLLER<<4) + channel
        self._check_run_stat(use_running_status, status)
        assert (0<=controller<=127), 'Illegal controller: %s' % controller
        assert (0<=value<=127), 'Illegal value: %s' % value
        self.set_running_status(c.CONTINUOUS_CONTROLLER, channel)


    def patch_change(self, channel, patch, use_running_status=False):
        """
        channel: 0-15
        patch: 0-127
        >>> MidiEvents().patch_change(0,120)
        >>> MidiEvents().patch_change(0,130)
        Traceback (most recent call last):
        ...
        AssertionError: Illegal patch: 130
        """
        self._check_ch(channel)
        status = (c.PATCH_CHANGE<<4) + channel
        self._check_run_stat(use_running_status, status)
        assert (0<=patch<=127), 'Illegal patch: %s' % patch


    def channel_pressure(self, channel, pressure, use_running_status=False):
        """
        channel: 0-15
        pressure: 0-127
        """
        self._check_ch(channel)
        status = (c.CHANNEL_PRESSURE<<4) + channel
        self._check_run_stat(use_running_status, status)
        assert (0<=pressure<=127), 'Illegal pressure: %s' % pressure


    def pitch_bend(self, channel, value, use_running_status=False):
        """
        channel: 0-15 - value: 0-16383
        >>> midi_out = MidiEvents()
        >>> midi_out.pitch_bend(1,65,True)
        Traceback (most recent call last):
        ...
        ValueError: status was: 225 - running status was: None. They MUST be the same when use_running_status==True
        >>> midi_out.set_running_status(225)
        >>> midi_out.pitch_bend(1,1337,True)
        >>> midi_out.get_running_status()
        225
        """
        self._check_ch(channel)
        status = (c.PITCH_BEND<<4) + channel
        self._check_run_stat(use_running_status, status)
        assert (0<=value<=32639), 'Illegal value: %s' %  value




    #####################
    ## System Exclusive

    def system_exclusive(self, data):
        """
        data: list of values in range(128)
        >>> MidiEvents().system_exclusive([0,2,127,34])
        >>> MidiEvents().system_exclusive([0,2,128,-2])
        Traceback (most recent call last):
        ...
        AssertionError: Some values in data out of range [128, -2]
        """
        illegals = [d for d in data if d>127 or d<0]
        assert (not illegals), 'Some values in data out of range %s' % repr(illegals)


    #####################
    ## Common events

    def song_position_pointer(self, song_position):
        """
        song_position: 0-16383
        """
        assert (0<=song_position<=16383), 'Illegal song_position: %s' % song_position

    def song_select(self, song_number):
        """
        song_number: 0-127
        """
        assert (0<=song_number<=127), 'Illegal song_number: %s' % song_number


    def tuning_request(self):
        """
        No values passed
        """
        pass

            
    def midi_time_code(self, msg_type, values):
        """
        msg_type: 0-7
        values: 0-15
        """
        assert (0<=msg_type<=7), 'Illegal msg_type: %s' % msg_type
        assert (0<=values<=15), 'Illegal values: %s' % values


    #########################
    # header does not really belong here. But anyhoo!!!
    
    def header(self, format=0, n_tracks=1, division=96):
        """
        format: type of midi file in [0,1,2]
        n_tracks: number of tracks (16 bit value) # I am unclear if having 0 tracks is legal as it makes no sense.
        division: (16 bit value) timing division
        >>> MidiEvents().header(0,1,2)
        >>> MidiEvents().header(0,65536,1)
        Traceback (most recent call last):
        ...
        AssertionError: n_tracks of tracks must be 0<=n_tracks<=0xffff. Was: 65536
        """
        assert (format in [0,1,2]), 'Illegal format: %s' % format
        assert (0<=n_tracks<=0xffff), 'n_tracks of tracks must be 0<=n_tracks<=0xffff. Was: %s' % n_tracks
        assert (0<=division<=0xffff), 'division of must be 0<=division<=0xffff. Was: %s' % division


    def eof(self):
        """
        End of file. No more events to be processed.
        """
        pass


    #####################
    ## meta events


    def meta_event(self, meta_type, data):
        """
        Handles any undefined meta events
        """
        pass


    def start_of_track(self, n_track=0):
        """
        n_track: number of track
        """
        assert (0<=n_track<=0xffff), 'n_track of tracks must be 0<=n_track<=0xffff. Was: %s' % n_track


    def end_of_track(self):
        """
        n_track: number of track
        """
        pass


    def sequence_number(self, seq_num):
        """
        seq_num: 0-16383
        """
        assert (0<=seq_num<=0x3fff), 'seq_num must be 0<=seq_num<=0x3fff. Was: %s' % seq_num


    def _assert_txt(self, text):
        "a legal midi text is an array of 8 bit bytes"
        bytes(text)


    def text(self, text):
        """
        Text event
        text: string
        >>> MidiEvents().text(b'Blow Wind Blow')
        >>> MidiEvents().text(b'midi will make me a \u0251 millionaire')
        Traceback (most recent call last):
        ...
        SyntaxError: bytes can only contain ASCII literal characters.
        >>> MidiEvents().text(bytes([1,2,255]))
        >>> MidiEvents().text(bytes([-1,2,256]))
        Traceback (most recent call last):
        ...
        ValueError: bytes must be in range(0, 256)
        """
        self._assert_txt(text)


    def copyright(self, text):
        """
        Copyright notice
        text: string
        """
        self._assert_txt(text)


    def sequence_name(self, text):
        """
        Sequence/track name
        text: string
        """
        self._assert_txt(text)


    def instrument_name(self, text):
        """
        text: string
        """
        self._assert_txt(text)


    def lyric(self, text):
        """
        """
        self._assert_txt(text)


    def marker(self, text):
        """
        text: string
        """
        self._assert_txt(text)


    def cuepoint(self, text):
        """
        text: string
        """
        self._assert_txt(text)


    def program_name(self, text):
        """
        text: string
        """
        self._assert_txt(text)


    def device_name(self, text):
        """
        text: string
        """
        self._assert_txt(text)


    def midi_ch_prefix(self, channel):
        """
        channel: midi channel for subsequent data (deprecated in the spec)
        """
        assert(0<=channel<=15)


    def midi_port(self, channel):
        """
        value: Midi port (deprecated in the spec)
        """
        assert(0<=channel<=15)


    def tempo(self, tempo):
        """
        value: 0-2097151
        tempo in us/quarternote
        (to calculate value from bpm: int(60,000,000.00 / BPM))
        >>> MidiEvents().tempo(60000000 / 85)
        >>> MidiEvents().tempo(-10)
        Traceback (most recent call last):
        ...
        AssertionError: Tempo in microseconds must be in the range 0..16777215. Was: -10
        """
        assert(0<=tempo<=16777215), 'Tempo in microseconds must be in the range 0..16777215. Was: %s' % tempo


    def tempo_bpm(self, bpm):
        "tempo in bpm. Just a helper. Not part of the midi spec"
        self.tempo(int(60000000/bpm))


    def smtp_offset(self, hour, minute, second, frame, framePart):
        """
        more: http://www.somascape.org/midi/tech/mfile.html#meta
        hour is a byte where different bits has different meaning.
        hour is encoded with the SMPTE format i.e. 0rrhhhhh, where :
            rr = frame rate :
                00 = 24 fps, 
                01 = 25 fps, 
                10 = 30 fps (drop frame), 
                11 = 30 fps (non-drop frame)
            hhhhh = hour (0-23)
        minute;: specifies the minutes (0-59)
         and seconds (0-59), respectively.
        frame is a byte specifying the number of frames (0-23/24/28/29, depending on the frame rate specified in the hr byte).
        framePart is a byte specifying the number of fractional frames, in 100ths of a frame 
        (even in SMPTE-based tracks using a different frame subdivision, defined in the MThd chunk).
        This optional event, if present, should occur at the start of a track, at time = 0, and prior to any MIDI events. 
        It is used to specify the SMPTE time at which the track is to start.
        For a format 1 MIDI file, a SMPTE Offset Meta event should only occur within the first MTrk chunk.

        >>> MidiEvents().smtp_offset(0b00100000+13, 37, 00, 24, 0)
        >>> MidiEvents().smtp_offset(0b01100000+13, 37, 00, 25, 0)
        >>> MidiEvents().smtp_offset(0b00100000+13, 37, 00, 31, 0)
        Traceback (most recent call last):
        ...
        AssertionError: Frame rate is 25 so frame must be in range 0..24 - was: 31
        """
        frame_rate = (hour&0b01100000)>>5
        hour_actual = (hour&0b00011111)
        assert(0<=hour_actual<=23), 'hour must be in the 0..23 range. Was: %s' % hour
        assert(0<=minute<=59), 'minute must be in the 0..59 range. Was: %s' % minute
        assert(0<=second<=59), 'second must be in the 0..59 range. Was: %s' % second
        if frame_rate == 0: # 24 fps
            assert(0<=frame<=23), 'Frame rate is 24 so frame must be in range 0..23 - was: %s' % frame
        elif frame_rate == 1: # 25 fps
            assert(0<=frame<=24), 'Frame rate is 25 so frame must be in range 0..24 - was: %s' % frame
        elif frame_rate == 2: # 30 fps (drop frame)
            assert(0<=frame<=28), 'Frame rate is 29 (drop frame) so frame must be in range 0..28 - was: %s' % frame
        elif frame_rate == 3: # 30 fps (non-drop frame)
            assert(0<=frame<=29), 'Frame rate is 30 (non-drop frame) so frame must be in range 0..29 - was: %s' % frame
        assert(0<=framePart<=99), 'framePart must be in 0..99 range. Was %s' % framePart


    def time_signature(self, nn, dd, cc, bb):
        """
        nn: Numerator of the signature as notated on sheet music
        dd: Denominator of the signature as notated on sheet music
            The denominator is a negative power of 2: 2 = quarter 
            note, 3 = eighth, etc.
        cc: The number of MIDI clocks in a metronome click
        bb: The number of notated 32nd notes in a MIDI quarter note 
            (24 MIDI clocks)
        """
        # I am not sure of these assertions. Must check with midi files.
        assert(0<=nn<=255), 'nn must be in 0..255 range. Was %s' % nn
        assert(0<=dd<=255), 'dd must be in 0..255 range. Was %s' % dd
        assert(0<=cc<=255), 'cc must be in 0..255 range. Was %s' % cc
        assert(0<=bb<=255), 'bb must be in 0..255 range. Was %s' % bb


    def key_signature(self, sf, mi):
        """
        sf: is a byte specifying the number of flats (-ve) or sharps 
            (+ve) that identifies the key signature (-7 = 7 flats, -1 
            = 1 flat, 0 = key of C, 1 = 1 sharp, etc).
        mi: is a byte specifying a major (0) or minor (1) key.
        >>> MidiEvents().key_signature(-121, 0)
        Traceback (most recent call last):
        ...
        AssertionError: sf must be in -7..7 range. Was -121
        """
        assert(-7<=sf<=7), 'sf must be in -7..7 range. Was %s' % sf
        assert(0<=mi<=1), 'mi must be in [0,1] range. Was %s' % mi


    def sequencer_specific(self, id, data):
        """
        FF 7F <len> <id> <data>
        data: The data as byte values
        >>> MidiEvents().sequencer_specific([0x41], [1,42,45])
        >>> MidiEvents().sequencer_specific([0], [1,42,45])
        Traceback (most recent call last):
        ...
        ValueError: Incorrect manufacturer id.
        >>> MidiEvents().sequencer_specific([0,0,56], [1,42,45])
        >>> MidiEvents().sequencer_specific([1,0,56], [1,42,45])
        Traceback (most recent call last):
        ...
        ValueError: Incorrect manufacturer id.
        >>> MidiEvents().sequencer_specific([0x41], [1,42,300])
        Traceback (most recent call last):
        ...
        AssertionError: Some values in data out of range [300]
        """
        id = bytes(id)
        manufacturer_id(id)
        assert(1<=len(id)<=3), 'length of id can be max 3 bytes, Was: %s' % len(id)
        illegals = [d for d in data if d>255 or d<0]
        assert (not illegals), 'Some values in data out of range %s' % repr(illegals)





    #####################
    ## realtime events

    def timing_clock(self):
        "No values passed"
        pass

    def song_start(self):
        "No values passed"
        pass

    def song_stop(self):
        "No values passed"
        pass

    def song_continue(self):
        "No values passed"
        pass

    def active_sensing(self):
        "No values passed"
        pass

    def system_reset(self):
        "No values passed"
        pass



if __name__ == '__main__':

    import doctest
    doctest.testmod() # run test on inline examples first
