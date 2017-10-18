# -*- coding: utf-8 -*-

# http://www.somascape.org/midi/tech/mfile.html
# http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html
# http://www.music-software-development.com/midi-tutorial.html
# https://www.csie.ntu.edu.tw/~r92092/ref/midi/
# http://midi.teragonaudio.com/tech/midispec.htm
# http://midi.teragonaudio.com/tech/midispec/run.htm
# http://www.recordingblogs.com/sa/Wiki/topic/Musical-Instrument-Digital-Interface-MIDI

from mxm.midifile.src import constants as c
from mxm.midifile.src.event_dispatcher import EventDispatcher

class OutTest:
    def header(self, format, nTracks, division):
        print (format, nTracks, division)
    def reset_running_status(self):
        self._running_status = None
    def set_running_status(self, status):
        self._running_status = status
    def reset_time(self):
        self.time = 0
    def set_current_track(self, n):
        self.current_track = n
    def start_of_track(self, current_track):
        print ('start_of_track: %s' % current_track)
    def update_time(self, new_time=0, relative=1):
        print('update_time: %s' % new_time)
    def note_on(self, channel, note, velocity, use_running_status=False):
        print ('note_on', channel, note, velocity, use_running_status)
    def note_off(self, channel, note, velocity, use_running_status=False):
        print ('note_off', channel, note, velocity, use_running_status)
    def eof(self):
        print('eof')

class MidiFileParser:
    """
    The MidiFileParser is the lowest level parser that see the data as 
    midi data. It generates events that gets triggered on the MidiEvents handler.
    >>> import io
    >>> from mxm.midifile import RawInstreamFile
    >>> from mxm.midifile.src.data_type_converters import writeBew, writeVar

    First we set up the header data for a simple midi file with 1 track
    >>> f = io.BytesIO()
    >>> mthd = b'MThd'
    >>> header_chunk_size = writeBew(6, 4)
    >>> format = writeBew(0, 2) # Format 0
    >>> nTracks = writeBew(1, 2) # One track
    >>> division = writeBew(480, 2) # 
    >>> mthd, list(header_chunk_size), list(format), list(nTracks), list(division)
    (b'MThd', [0, 0, 0, 6], [0, 0], [0, 1], [1, 224])
    >>> (f.write(mthd), f.write(header_chunk_size), f.write(format), f.write(nTracks), f.write(division))
    (4, 4, 2, 2, 2)

    Then we set up some track data
    >>> tracklength = 0
    >>> start_time = bytes(writeVar(0))
    >>> tracklength += len(start_time)
    >>> note_on = bytes([0x90, 64, 64])
    >>> tracklength += len(note_on)
    >>> note_off_time = bytes(writeVar(96))
    >>> tracklength += len(note_off_time)
    >>> note_off = bytes([0x80, 64, 64])
    >>> tracklength += len(note_off)
    >>> (f.write(b'MTrk'), f.write(writeBew(tracklength, 4)), f.write(start_time), f.write(note_on), f.write(note_off_time), f.write(note_off))
    (4, 4, 1, 3, 1, 3)

    And finally we parse the data, first the metadata
    >>> r_in = RawInstreamFile(f)
    >>> p = MidiFileParser(r_in, OutTest())
    >>> p.parseMThdChunk()
    0 1 480
    
    then the tracks
    >>> p.parseMTrkChunks()
    start_of_track: 0
    update_time: 0
    note_on 0 64 64 False
    update_time: 96
    note_off 0 64 64 False
    eof
    """

    def __init__(self, raw_in, event_handler):
        """
        raw_data is the raw content of a midi file as bytes.
        """
        # internal values, don't mess with 'em directly
        self.raw_in = raw_in
        self.dispatch = EventDispatcher(event_handler)
        # running status is only implemented for Voice Category messages (ie, Status is 0x80 to 0xEF).
        self.reset_running_status()

    def reset_running_status(self):
        self._running_status = None
        self._use_running_status = False
        self.dispatch.reset_running_status()
        
    def set_running_status(self, status):
        self._running_status = status
        self.dispatch.set_running_status(status)

    def get_running_status(self):
        return self._running_status


    def parseMThdChunk(self):
        """
        Parses the header chunk
        """
        raw_in = self.raw_in
        header_chunk_type = raw_in.nextSlice(4)
        header_chunk_size = raw_in.readBew(4)
        # check if it is a proper midi file
        if bytes(header_chunk_type) != b'MThd':
            raise TypeError("ERROR: It is not a valid midi file!")
        # Header values are at fixed locations, so no reason to be clever
        self.format = raw_in.readBew(2)
        self.nTracks = raw_in.readBew(2)
        self.division = raw_in.readBew(2)
        # Theoretically a header larger than 6 bytes can exist
        # but no one has seen one in the wild
        # But correctly ignore unknown data if it is though
        if header_chunk_size > 6:
            raw_in.moveCursor(header_chunk_size-6)
        # call the header event handler on the stream
        self.dispatch.header(self.format, self.nTracks, self.division)


    def parseMTrkChunks(self):
        "Parses all track chunks."
        for t in range(self.nTracks):
            self._current_track = t
            self.parseMTrkChunk() # this is where it's at!
        self.dispatch.eof()


    def parseMTrkChunk(self):
        "Parses a track chunk. This is the most important part of the parser."
        # set time to 0 at start of a track
        self.dispatch.reset_time()
        dispatch = self.dispatch
        raw_in = self.raw_in
#        print('raw_in.data[raw_in.getCursor():raw_in.getCursor()+20] %s' % raw_in.data[raw_in.getCursor():raw_in.getCursor()+20] )
#        print('raw_in.data[raw_in.getCursor():raw_in.getCursor()+20] %s' % list(raw_in.data[raw_in.getCursor():raw_in.getCursor()+20]) )
        # Trigger event at the start of a track
        dispatch.start_of_track(self._current_track)
        # position cursor after track header
        raw_in.moveCursor(4)
        # unsigned long is 4 bytes
        tracklength = raw_in.readBew(4)
#        print ('tracklength: %s' % tracklength)
        track_endposition = raw_in.getCursor() + tracklength # absolute position!

#        print(raw_in.data[raw_in.getCursor():raw_in.getCursor()+20]) 
#        print(list(raw_in.data[raw_in.getCursor():raw_in.getCursor()+20]))

        while raw_in.getCursor() < track_endposition:
            
            # find relative time of the event
            time = raw_in.readVarLen()
            dispatch.update_time(time)
            
            # running status is only implemented for Voice Category
            # messages (ie, Status is 0x80 to 0xEF).
            peak_ahead = raw_in.readBew(move_cursor=0)
#            print('peak_ahead: %s' % peak_ahead)
            if (peak_ahead & 0b10000000): 
                # the status byte has the high bit set, so it
                # was not running data but proper status byte
                status = raw_in.readBew()
                self.set_running_status(status)
                self._use_running_status = False
            else:
                # use that darn running status
                status = self.get_running_status()
                self._use_running_status = True

                # while I am almost certain that no realtime 
                # messages will pop up in a midi file, I might need to 
                # change my mind later.

            # we need to look at nibbles here
#            print('='*80)
#            print (status)
            hi_nible, lo_nible = (status & 0xF0) >> 4, status & 0x0F
            if hi_nible == 0xF:
                self.reset_running_status()
            
            # match up with events

            # Is it a meta_event ??
            # these only exists in midi files, not in transmitted midi data
            # In transmitted data META_EVENT (0xFF) is a system reset
            if status == c.META_EVENT:
                meta_type = raw_in.readBew()
                meta_length = raw_in.readVarLen()
                meta_data = raw_in.nextSlice(meta_length)
                dispatch.meta_event(meta_type, meta_data)


            # Is it a sysex_event ??
            elif status == c.SYSTEM_EXCLUSIVE:
                # ignore sysex events
                sysex_length = raw_in.readVarLen()
                # don't read sysex terminator
                sysex_data = raw_in.nextSlice(sysex_length-1)
                # only read last data byte if it is a sysex terminator
                # It should allways be there, but better safe than sorry
                if raw_in.readBew(move_cursor=0) == c.END_OFF_EXCLUSIVE:
                    eo_sysex = raw_in.readBew()
                dispatch.sysex_event(sysex_data)
                # the sysex code has not been properly tested, and might be fishy!


            # is it a system common event?
            elif hi_nible == 0xF0: # Hi bits are set then
                data_sizes = {
                    c.MTC:1,
                    c.SONG_POSITION_POINTER:2,
                    c.SONG_SELECT:1,
                }
                data_size = data_sizes.get(hi_nible, 0)
                common_data = raw_in.nextSlice(data_size)
                common_type = lo_nible
                dispatch.system_common(common_type, common_data)
            

            # Oh! Then it must be a midi event (channel voice message)
            else:
                data_sizes = {
                    c.PATCH_CHANGE:1,
                    c.CHANNEL_PRESSURE:1,
                    c.NOTE_OFF:2,
                    c.NOTE_ON:2,
                    c.AFTERTOUCH:2,
                    c.CONTINUOUS_CONTROLLER:2,
                    c.PITCH_BEND:2,
                }
                data_size = data_sizes.get(hi_nible, 0)
                channel_data = raw_in.nextSlice(data_size)
                event_type, channel = hi_nible, lo_nible
#                print ((event_type, channel, channel_data, self._use_running_status))
                dispatch.channel_message(event_type, channel, channel_data, self._use_running_status)



if __name__ == '__main__':

    import doctest
    doctest.testmod() # run test on inline examples first

    # # get data
    # test_file = '/home/maxm/instances/midienv/mxm.midifile-1.0/mxm/midifile/tests/midifiles/midiout-0001.mid'

    # # do parsing
    # from mxm.midifile import MidiToCode
    # from  mxm.midifile import RawInstreamFile

    # midi_in = MidiFileParser(RawInstreamFile(test_file), MidiToCode())
    # midi_in.parseMThdChunk()
    # midi_in.parseMTrkChunks()
    
