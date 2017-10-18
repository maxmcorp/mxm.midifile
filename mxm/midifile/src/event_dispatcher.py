# -*- coding: utf-8 -*-

# custom
from mxm.midifile.src.data_type_converters import readBew, readVar, varLen, from_twos_complement, to_twos_complement
from mxm.midifile.src import constants as c

class EventDispatcher:

    def __init__(self, event_handler):
        
        """
        The event dispatcher generates events on the event_handler.
        """
        
        # internal values, don't mess with 'em directly
        self.event_handler = event_handler
        
        # public flags

        # A note_on with a velocity of 0x00 is actually the same as a 
        # note_off with a velocity of 0x40. When 
        # "convert_zero_velocity" is set, the zero velocity note_on's 
        # automatically gets converted into note_off's. This is a less 
        # suprising behaviour for those that are not into the intimate 
        # details of the midi spec.
        self.convert_zero_velocity = False
        
        # If dispatch_continuos_controllers is true, continuos 
        # controllers gets dispatched to their defined handlers. Else 
        # they just trigger the "continuous_controller" event handler.
        self.dispatch_continuos_controllers = 1 # NOT IMPLEMENTED YET
        
        # If dispatch_meta_events is true, meta events get's dispatched 
        # to their defined events. Else they all they trigger the 
        # "meta_event" handler.
        self.dispatch_meta_events = 1



    def header(self, format, nTracks, division):
        "Triggers the header event"
        self.event_handler.header(format, nTracks, division)


    def start_of_track(self, current_track):
        "Triggers the start of track event"
        self.event_handler.set_current_track(current_track)
        self.event_handler.start_of_track(current_track)
        
    
    def sysex_event(self, data): # files use sequencer specific, sysex is for live midi
        "Dispatcher for sysex events"
        self.event_handler.sysex_event(data)
    
    
    def eof(self):
        "End of file!"
        self.event_handler.eof()


    def update_time(self, new_time=0, relative=1):
        "Updates relative/absolute time."
        self.event_handler.update_time(new_time=new_time, relative=relative)
        
        
    def reset_time(self):
        "Updates relative/absolute time."
        self.event_handler.reset_time()


    # wrapping the oueventss running stat methods

    def set_running_status(self, *args):
        "set the running status"
        self.event_handler.set_running_status(*args)

    def get_running_status(self):
        "Get the running status"
        self.event_handler.get_running_status()

    def reset_running_status(self):
        "reset the running status"
        self.event_handler.reset_running_status()



    # Event dispatchers for similar types of events
    
    
    def channel_message(self, hi_nible, channel, data, use_running_status=False):
        """
        Dispatches channel messages
        """
        events = self.event_handler
        if (c.NOTE_ON) == hi_nible:
            note, velocity = data
            # note_on with velocity 0x00 are same as note 
            # off with velocity 0x40 according to spec!
            if velocity==0 and self.convert_zero_velocity:
                events.note_off(channel, note, 0x40, use_running_status)
            else:
                events.note_on(channel, note, velocity, use_running_status)
        elif (c.NOTE_OFF) == hi_nible:
            note, velocity = data
            events.note_off(channel, note, velocity, use_running_status)
        elif (c.AFTERTOUCH) == hi_nible:
            note, velocity = data
            events.aftertouch(channel, note, velocity, use_running_status)
        elif (c.CONTINUOUS_CONTROLLER) == hi_nible:
            controller, value = data
            # A lot of the cc's are defined, so we trigger those directly
            if self.dispatch_continuos_controllers:
                self.continuous_controllers(channel, controller, value, use_running_status)
            else:
                events.continuous_controller(channel, controller, value, use_running_status)
        elif (c.PATCH_CHANGE) == hi_nible:
            program = data[0]
            events.patch_change(channel, program, use_running_status)
        elif (c.CHANNEL_PRESSURE) == hi_nible:
            pressure = data[0]
            events.channel_pressure(channel, pressure, use_running_status)
        elif (c.PITCH_BEND) == hi_nible:
            hibyte, lobyte = data
            value = (hibyte<<7) + lobyte
            events.pitch_bend(channel, value, use_running_status)
        else:
            raise ValueError('Illegal channel message! %.x' % hi_nible)


    def continuous_controllers(self, channel, controller, value, use_running_status):
        """
        Dispatches continuous_controllers messages
        """
        events = self.event_handler
        # I am not really shure if I ought to dispatch continuous controllers
        # There's so many of them that it can clutter up the MidiEvents 
        # classes.
        # So I just trigger the default event handler
        events.continuous_controller(channel, controller, value, use_running_status)



    def system_commons(self, common_type, common_data):
    
        "Dispatches system common messages"
        
        events = self.event_handler
        
        # MTC Midi time code Quarter value
        if common_type == c.MTC:
            data = readBew(common_data)
            msg_type = (data & 0x07) >> 4
            values = (data & 0x0F)
            events.midi_time_code(msg_type, values)
        elif common_type == c.SONG_POSITION_POINTER:
            hibyte, lobyte = common_data
            value = (hibyte<<7) + lobyte
            events.song_position_pointer(value)
        elif common_type == c.SONG_SELECT:
            data = readBew(common_data)
            events.song_select(data)
        elif common_type == c.TUNING_REQUEST:
            # no data then
            events.tuning_request(time=None)



    def meta_event(self, meta_type, data):
        "Dispatches meta events"
        events = self.event_handler
        
        # SEQUENCE_NUMBER = 0x00 (00 02 ss ss (seq-number))
        if meta_type == c.SEQUENCE_NUMBER:
            number = readBew(data)
            events.sequence_number(number)
        
        # TEXT = 0x01 (01 len text...)
        elif meta_type == c.TEXT:
            events.text(data)
        
        # COPYRIGHT = 0x02 (02 len text...)
        elif meta_type == c.COPYRIGHT:
            events.copyright(data)
        
        # SEQUENCE_NAME = 0x03 (03 len text...)
        elif meta_type == c.SEQUENCE_NAME:
            events.sequence_name(data)
        
        # INSTRUMENT_NAME = 0x04 (04 len text...)
        elif meta_type == c.INSTRUMENT_NAME:
            events.instrument_name(data)
        
        # LYRIC = 0x05 (05 len text...)
        elif meta_type == c.LYRIC:
            events.lyric(data)
        
        # MARKER = 0x06 (06 len text...)
        elif meta_type == c.MARKER:
            events.marker(data)
        
        # CUEPOINT = 0x07 (07 len text...)
        elif meta_type == c.CUEPOINT:
            events.cuepoint(data)
        
        # PROGRAM_NAME = 0x08 (05 len text...)
        elif meta_type == c.PROGRAM_NAME:
            events.program_name(data)
        
        # DEVICE_NAME = 0x09 (09 len text...)
        elif meta_type == c.DEVICE_NAME:
            events.device_name(data)
        
        # MIDI_CH_PREFIX = 0x20 (20 01 channel)
        elif meta_type == c.MIDI_CH_PREFIX:
            channel = readBew(data)
            events.midi_ch_prefix(channel)
        
        # MIDI_PORT  = 0x21 (21 01 port (legacy stuff))
        elif meta_type == c.MIDI_PORT:
            port = readBew(data)
            events.midi_port(port)
        
        # END_OFF_TRACK = 0x2F (2F 00)
        elif meta_type == c.END_OF_TRACK:
            events.end_of_track()
        
        # TEMPO = 0x51 (51 03 tt tt tt (tempo in us/quarternote))
        elif meta_type == c.TEMPO:
            b1, b2, b3 = data
            # uses 3 bytes to represent time between quarter 
            # notes in microseconds
            events.tempo((b1<<16) + (b2<<8) + b3)
        
        # SMTP_OFFSET = 0x54 (0x54 05 hh mm ss ff xx)
        elif meta_type == c.SMTP_OFFSET:
            hour, minute, second, frame, framePart = data
            events.smtp_offset(
                    hour, minute, second, frame, framePart)
        
        # TIME_SIGNATURE = 0x58 (58 04 nn dd cc bb)
        elif meta_type == c.TIME_SIGNATURE:
            nn, dd, cc, bb = data
            events.time_signature(nn, dd, cc, bb)
        
        # KEY_SIGNATURE = 0x59 (59 02 sf mi)
        elif meta_type == c.KEY_SIGNATURE:
            sf, mi = data
            sf = from_twos_complement(sf)
            events.key_signature(sf, mi)
        
        # SPECIFIC = 0x7F (Sequencer specific event)
        elif meta_type == c.SEQUENCER_SPECIFIC:
            meta_data = data
            if meta_data[0] == 0:
                id = meta_data[:3]
                meta_data = meta_data[3:]
            else:
                id = meta_data[0:1]
                meta_data = meta_data[1:]
            events.sequencer_specific(id, meta_data)
        
        # Handles any undefined meta events
        else: # undefined meta type
            meta_data = data
            events.meta_event(meta_type, meta_data)





if __name__ == '__main__':

    import doctest
    doctest.testmod() # run test on inline examples first
