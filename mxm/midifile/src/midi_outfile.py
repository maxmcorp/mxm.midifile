# -*- coding: utf-8 -*-

from mxm.midifile.src import constants as c
from mxm.midifile.src.midi_events import MidiEvents
from mxm.midifile.src.raw_outstream_file import RawOutstreamFile
from mxm.midifile.src.data_type_converters import writeVar, writeBew, to_twos_complement

class MidiOutFile(MidiEvents):

    """
    MidiOutFile is an eventhandler that subclasses MidiEvents 
    and writes midi events to it.
    >>> midi_out = MidiOutFile()
    >>> midi_out.note_on(0,64,127)
    Traceback (most recent call last):
    ...
    AttributeError: '_current_track_buffer' is not found. Did you forget to call 'start_of_track()'
    >>> midi_out.start_of_track()
    >>> midi_out.note_on(0,64,127)
    >>> list(midi_out._current_track_buffer.read_all())
    [0, 144, 64, 127]
    >>> midi_out.close()
    """

    def __init__(self, f=''):
        if f and isinstance(f, str):
            f = open(f, 'wb')
        self.raw_out = RawOutstreamFile(f)
        MidiEvents.__init__(self)

    def write(self):
        self.raw_out.write()

    def read_all(self):
        "mainly for testing"
        return self.raw_out.read_all()

    def close(self):
        "self"
        self.raw_out.close()
        if hasattr(self, '_current_track_buffer'):
            self._current_track_buffer.close()

    def event_slice(self, slc):
        """
        Writes the slice of an event to the current track. Correctly 
        inserting a varlen timestamp too.
        start_of_track MUST be called before calling this.
        """
        if not hasattr(self, '_current_track_buffer'):
            raise AttributeError("'_current_track_buffer' is not found. Did you forget to call 'start_of_track()'")
        current = self._current_track_buffer
        current.writeVarLen(self.rel_time())
        current.writeSlice(slc)

    
    #####################
    ## Midi events


    def note_on(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
        """
        channel: 0-15
        note, velocity: 0-127
        """
        super().note_on(channel=channel, note=note, velocity=velocity, use_running_status=use_running_status)
        if use_running_status:
            slc = [note, velocity]
        else:
            status = (c.NOTE_ON<<4) + channel
            slc = [status, note, velocity]
        self.event_slice(slc)


    def note_off(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
        """
        channel: 0-15
        note, velocity: 0-127
        """
        super().note_off(channel=channel, note=note, velocity=velocity, use_running_status=use_running_status)
        if use_running_status:
            slc = [note, velocity]
        else:
            status = (c.NOTE_OFF<<4) + channel
            slc = [status, note, velocity]
        self.event_slice(slc)


    def aftertouch(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
        """
        channel: 0-15
        note, velocity: 0-127
        """
        super().aftertouch(channel, note, velocity, use_running_status=use_running_status)
        if use_running_status:
            slc = [note, velocity]
        else:
            slc = [(c.AFTERTOUCH<<4) + channel, note, velocity]
        self.event_slice(slc)


    def continuous_controller(self, channel, controller, value, use_running_status=False):
        """
        channel: 0-15
        controller, value: 0-127
        """
        super().continuous_controller(channel, controller, value, use_running_status=use_running_status)
        if use_running_status:
            slc = [controller, value]
        else:
            slc = [(c.CONTINUOUS_CONTROLLER<<4) + channel, controller, value]
        self.event_slice(slc)
        # These should probably be implemented
        # http://users.argonet.co.uk/users/lenny/midi/tech/spec.html#ctrlnums


    def patch_change(self, channel, patch, use_running_status=False):
        """
        channel: 0-15
        patch: 0-127
        """
        super().patch_change(channel, patch, use_running_status=use_running_status)
        if use_running_status:
            slc = [patch]
        else:
            slc = [(c.PATCH_CHANGE<<4) + channel, patch]
        self.event_slice(slc)


    def channel_pressure(self, channel, pressure, use_running_status=False):

        """
        channel: 0-15
        pressure: 0-127
        """
        super().channel_pressure(channel, pressure, use_running_status=use_running_status)
        if use_running_status:
            slc = [pressure]
        else:
            slc = [(c.CHANNEL_PRESSURE<<4) + channel, pressure]
        self.event_slice(slc)


    def pitch_bend(self, channel, value, use_running_status=False):

        """
        channel: 0-15
        value: 0-16383
        """
        super().pitch_bend(channel, value, use_running_status=use_running_status)
        msb = (value>>7) & 0xFF
        lsb = value & 0xFF
        if use_running_status:
            slc = [msb, lsb]
        else:
            slc = [(c.PITCH_BEND<<4) + channel, msb, lsb]
        self.event_slice(slc)




    #####################
    ## System Exclusive

    def sysex_event(self, data):
        """
        data: list of values in range(128)
        """
        super().system_exclusive(data)
        sysex_slice = bytearray([c.SYSTEM_EXCLUSIVE])
        sysex_slice += bytearray(writeVar(len(data)+1)) # sysex_len
        sysex_slice += data
        sysex_slice += bytearray([c.END_OFF_EXCLUSIVE])
        self.event_slice(sysex_slice)


    #####################
    ## Common events

    def midi_time_code(self, msg_type, values):
        """
        msg_type: 0-7
        values: 0-15
        """
        super().midi_time_code(msg_type, values)
        value = (msg_type<<4) + values
        self.event_slice([c.MIDI_TIME_CODE, value])


    def song_position_pointer(self, value):
        """
        value: 0-16383
        """
        super().song_position_pointer(value)
        lsb = (value & 0x7F)
        msb = (value >> 7) & 0x7F
        self.event_slice([c.SONG_POSITION_POINTER, lsb, msb])


    def song_select(self, songNumber):
        """
        songNumber: 0-127
        """
        super().song_select(songNumber)
        self.event_slice([c.SONG_SELECT, songNumber])


    def tuning_request(self):
        """
        No values passed
        """
        super().tuning_request()
        self.event_slice(chr(c.TUNING_REQUEST))

            
    #########################
    # header does not really belong here. But anyhoo!!!
    
    def header(self, format=0, nTracks=1, division=96):
        """
        format: type of midi file in [0,1,2]
        nTracks: number of tracks. 1 track for type 0 file
        division: timing division ie. 96 ppq.
        This may be in either of two formats, depending on the value of MS bit:
        (0b0nnnnnnn, 0bnnnnnnnn): ticks per quarter note
        (0b1nnnnnnn, 0bnnnnnnnn): (-frames per second, ticks per frame)
        >>> midi_out = MidiOutFile()
        >>> midi_out.header(format=0, nTracks=1, division=96)
        >>> midi_out.read_all()[:4]
        b'MThd'
        >>> l = list(midi_out.read_all())
        >>> header, size, format, nTracks, division = \
                l[0:4], l[4:8], l[8:10], l[10:12], l[12:14]
        >>> header, size, format, nTracks, division
        ([77, 84, 104, 100], [0, 0, 0, 6], [0, 0], [0, 1], [0, 96])
        """        
        raw = self.raw_out
        raw.writeSlice(c.FILE_HEADER)
        bew = raw.writeBew
        bew(6, 4) # header size
        bew(format, 2)
        bew(nTracks, 2)
        bew(division, 2)


    def eof(self):
        """
        End of file. No more events to be processed.
        A hook to do something at end of parsing.
        """
        


    #####################
    ## meta events. these happens inside tracks


    def meta_slice(self, meta_type, data_slice):
        """
        Writes a meta event. meta_type is a byte from constants. data_slice is bytes
        >>> midi_out = MidiOutFile()
        >>> midi_out.start_of_track()
        >>> midi_out.meta_slice(meta_type=c.TEXT, data_slice=b'pimpf')
        >>> midi_out.end_of_track()
        >>> r = list(midi_out.read_all())
        >>> bytes(r[12:17])
        b'pimpf'
        """
        slc = bytearray()
        slc.append(c.META_EVENT) # this is a meta event
        slc.append(meta_type)    # the specific meta event.
        slc += bytes(writeVar(len(data_slice)))
        slc += data_slice
        self.event_slice(slc)


    def meta_event(self, meta_type, data):
        """
        Handles any undefined meta events
        """
        self.meta_slice(meta_type, data)


    def start_of_track(self, n_track=0):
        """
        n_track: number of track
        """
        super().start_of_track(n_track)
        self._current_track_buffer = RawOutstreamFile()
        self.reset_time()
        self._current_track += 1


    def end_of_track(self):
        """
        Writes the track to the buffer.
        >>> from mxm.midifile.src.data_type_converters import readBew
        >>> midi_out = MidiOutFile()
        >>> midi_out.start_of_track()
        >>> midi_out.note_on(channel=0, note=0x40, velocity=0x40)
        >>> midi_out.end_of_track()
        >>> r = list(midi_out.read_all())
        >>> r
        [77, 84, 114, 107, 0, 0, 0, 8, 0, 144, 64, 64, 0, 255, 47, 0]
        >>> bytes(r[:4]), readBew(r[4:8]), r[8:12], r[12:16]
        (b'MTrk', 8, [0, 144, 64, 64], [0, 255, 47, 0])
        """
        raw = self.raw_out
        raw.writeSlice(c.TRACK_HEADER)
        # track_data = self._current_track_buffer.getvalue()
        track_data = self._current_track_buffer.read_all()
        eot_slice = bytes(writeVar(self.rel_time())) + bytes([c.META_EVENT, c.END_OF_TRACK, 0])
        # wee need to know size of track data.
        track_length = len(track_data)+len(eot_slice)
        raw.writeBew(track_length, 4)
        # then write
        raw.writeSlice(track_data)
        raw.writeSlice(eot_slice)
        self._current_track_buffer.close()
        del self._current_track_buffer
        


    def sequence_number(self, value):
        """
        value: 0-65535
        This is an optional event, which must occur only at the start of a track,
        before any non-zero delta-time. 
        >>> midi_out = MidiOutFile()
        >>> midi_out.start_of_track()
        >>> midi_out.sequence_number(42)
        >>> midi_out.end_of_track()
        >>> r = list(midi_out.read_all())
        >>> (r[14]<<8) + r[15]
        42
        """
        super().sequence_number(value)
        self.meta_slice(c.SEQUENCE_NUMBER, writeBew(0, 2)+writeBew(value, 2))


    def text(self, text):
        """
        Text event, text: bytes
        >>> midi_out = MidiOutFile()
        >>> midi_out.start_of_track()
        >>> midi_out.text(b'1234')
        >>> r = midi_out._current_track_buffer.read_all()
        >>> list(r)
        [0, 255, 1, 4, 49, 50, 51, 52]
        """
        super().text(text)
        self.meta_slice(c.TEXT, bytes(text))


    def copyright(self, text):
        """
        Copyright notice, text: bytes
        """
        super().copyright(text)
        self.meta_slice(c.COPYRIGHT, bytes(text))


    def sequence_name(self, text):
        """
        Sequence/track name, text: bytes
        """
        super().sequence_name(text)
        self.meta_slice(c.SEQUENCE_NAME, bytes(text))


    def instrument_name(self, text):
        """
        text: bytes
        """
        super().instrument_name(text)
        self.meta_slice(c.INSTRUMENT_NAME, bytes(text))


    def lyric(self, text):
        """
        text: bytes
        """
        super().lyric(text)
        self.meta_slice(c.LYRIC, bytes(text))


    def marker(self, text):
        """
        text: bytes
        """
        super().marker(text)
        self.meta_slice(c.MARKER, bytes(text))


    def cuepoint(self, text):
        """
        text: bytes
        """
        super().cuepoint(text)
        self.meta_slice(c.CUEPOINT, bytes(text))


    def program_name(self, text):
        """
        text: bytes
        """
        super().program_name(text)
        self.meta_slice(c.PROGRAM_NAME, bytes(text))


    def device_name(self, text):
        """
        text: bytes
        """
        super().device_name(text)
        self.meta_slice(c.DEVICE_NAME, bytes(text))



    def midi_ch_prefix(self, channel):
        """
        channel: midi channel for subsequent data
        (deprecated in the spec)
        >>> midi_out = MidiOutFile()
        >>> midi_out.start_of_track()
        >>> midi_out.midi_ch_prefix(12)
        >>> midi_out.end_of_track()
        >>> list(midi_out.read_all())
        [77, 84, 114, 107, 0, 0, 0, 9, 0, 255, 32, 1, 12, 0, 255, 47, 0]
        """
        super().midi_ch_prefix(channel)
        self.meta_slice(c.MIDI_CH_PREFIX, bytes([channel]))


    def midi_port(self, value):

        """
        value: Midi port (deprecated in the spec)
        >>> midi_out = MidiOutFile()
        >>> midi_out.start_of_track()
        >>> midi_out.midi_port(4)
        >>> midi_out.end_of_track()
        >>> list(midi_out.read_all())
        [77, 84, 114, 107, 0, 0, 0, 9, 0, 255, 32, 1, 4, 0, 255, 47, 0]
        """
        self.meta_slice(c.MIDI_CH_PREFIX, bytes([value]))


    def tempo(self, value):
        """
        value: 0-2097151
        tempo in us/quarternote
        (to calculate value from bpm: int(60,000,000.00 / BPM))
        """
        value = int(value)
        super().tempo(value)
        hb, mb, lb = (value>>16 & 0xff), (value>>8 & 0xff), (value & 0xff)
        data_slice = bytes([hb, mb, lb])
        self.meta_slice(c.TEMPO, data_slice)


    def smtp_offset(self, hour, minute, second, frame, framePart):

        """
        hour,
        minute,
        second: 3 bytes specifying the hour (0-23), minutes (0-59) and 
                seconds (0-59), respectively. The hour should be 
                encoded with the SMPTE format, just as it is in MIDI 
                Time Code.
        frame: A byte specifying the number of frames per second (one 
               of : 24, 25, 29, 30).
        framePart: A byte specifying the number of fractional frames, 
                   in 100ths of a frame (even in SMPTE-based tracks 
                   using a different frame subdivision, defined in the 
                   MThd chunk).
        """
        super().smtp_offset(hour, minute, second, frame, framePart)
        data_slice = bytes([hour, minute, second, frame, framePart])
        self.meta_slice(c.SMTP_OFFSET, data_slice)



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
        super().time_signature(nn, dd, cc, bb)
        data_slice = bytes([nn, dd, cc, bb])
        self.meta_slice(c.TIME_SIGNATURE, data_slice)


    def key_signature(self, sf, mi):
        """
        sf: is a byte specifying the number of flats (-ve) or sharps 
            (+ve) that identifies the key signature (-7 = 7 flats, -1 
            = 1 flat, 0 = key of C, 1 = 1 sharp, etc).
        mi: is a byte specifying a major (0) or minor (1) key.
        """
        super().key_signature(sf, mi)
        sf = to_twos_complement(sf)
        data_slice = bytes([sf, mi])
        self.meta_slice(c.KEY_SIGNATURE, data_slice)



    def sequencer_specific(self, id, data):
        """
        id: manufacturer id. 1 or 3 bytes long.
        data: The data as byte values
        """
        super().sequencer_specific(id, data)
        data = bytes(data)
        len_data = len(id) + len(data)
        len_data = writeVar(len_data)
        seq_slice = bytes(len_data) + bytes(id) + data
        self.meta_slice(c.SEQUENCER_SPECIFIC, seq_slice)





#    #####################
#    ## realtime events

#    These are of no use in a midi file, so they are ignored!!!

#    def timing_clock(self):
#    def song_start(self):
#    def song_stop(self):
#    def song_continue(self):
#    def active_sensing(self):
#    def system_reset(self):



if __name__ == '__main__':

    import doctest
    doctest.testmod() # run test on inline examples first
