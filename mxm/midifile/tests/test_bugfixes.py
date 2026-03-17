# -*- coding: utf-8 -*-

"""
Tests for bugfixes applied to the mxm.midifile library.
"""

import io
import unittest

from mxm.midifile.src import constants as c
from mxm.midifile.src.data_type_converters import writeBew, writeVar
from mxm.midifile.src.midi_events import MidiEvents
from mxm.midifile.src.midi_outfile import MidiOutFile
from mxm.midifile.src.midi_file_parser import MidiFileParser


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class EventCollector(MidiEvents):
    """Event handler that records dispatched events for assertions."""

    def __init__(self):
        super().__init__()
        self.events = []

    def start_of_track(self, n_track=0):
        self.events.append(('start_of_track', n_track))

    def note_on(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
        super().note_on(channel, note, velocity, use_running_status)
        self.events.append(('note_on', channel, note, velocity))

    def note_off(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
        super().note_off(channel, note, velocity, use_running_status)
        self.events.append(('note_off', channel, note, velocity))

    def meta_event(self, meta_type, data):
        self.events.append(('meta_event', meta_type, data))

    def sysex_event(self, data):
        self.events.append(('sysex_event', data))

    def midi_time_code(self, msg_type, values):
        super().midi_time_code(msg_type, values)
        self.events.append(('midi_time_code', msg_type, values))

    def song_position_pointer(self, value):
        super().song_position_pointer(value)
        self.events.append(('song_position_pointer', value))

    def song_select(self, song_number):
        super().song_select(song_number)
        self.events.append(('song_select', song_number))

    def tuning_request(self):
        super().tuning_request()
        self.events.append(('tuning_request',))

    def channel_message(self, event_type, channel, channel_data, use_running_status=False):
        self.events.append(('channel_message', event_type, channel, bytes(channel_data)))

    def eof(self):
        self.events.append(('eof',))


def _end_of_track():
    """Return bytes for a delta-time-0 end-of-track meta event."""
    return bytes(writeVar(0)) + bytes([0xFF, 0x2F, 0x00])


def _build_midi_bytes(track_bytes, append_eot=True):
    """Build a minimal format-0 MIDI file with one track from raw track content bytes."""
    if append_eot:
        track_bytes = track_bytes + _end_of_track()
    f = io.BytesIO()
    # MThd
    f.write(b'MThd')
    f.write(writeBew(6, 4))
    f.write(writeBew(0, 2))   # format 0
    f.write(writeBew(1, 2))   # 1 track
    f.write(writeBew(480, 2)) # division
    # MTrk
    f.write(b'MTrk')
    f.write(writeBew(len(track_bytes), 4))
    f.write(track_bytes)
    return f


# ---------------------------------------------------------------------------
# Fix 1: System common data_size lookup used hi_nible instead of status
# ---------------------------------------------------------------------------

class TestSystemCommonParsing(unittest.TestCase):

    def _parse(self, track_data):
        f = _build_midi_bytes(track_data)
        collector = EventCollector()
        from mxm.midifile import RawInstreamFile
        parser = MidiFileParser(RawInstreamFile(f), collector)
        parser.parseMThdChunk()
        parser.parseMTrkChunks()
        return collector

    def test_mtc_quarter_frame(self):
        """MTC (0xF1) should be parsed and dispatched as midi_time_code."""
        # 0xF1 data_byte: high nibble = msg_type, low nibble = values
        track_data = bytes(writeVar(0)) + bytes([0xF1, 0x23])
        collector = self._parse(track_data)
        mtc_events = [e for e in collector.events if e[0] == 'midi_time_code']
        self.assertEqual(len(mtc_events), 1)

    def test_song_position_pointer(self):
        """Song Position Pointer (0xF2) should read 2 data bytes."""
        track_data = bytes(writeVar(0)) + bytes([0xF2, 0x10, 0x20])
        collector = self._parse(track_data)
        spp_events = [e for e in collector.events if e[0] == 'song_position_pointer']
        self.assertEqual(len(spp_events), 1)
        # value = (hibyte<<7) + lobyte = (0x10<<7) + 0x20 = 2080
        self.assertEqual(spp_events[0][1], (0x10 << 7) + 0x20)

    def test_song_select(self):
        """Song Select (0xF3) should read 1 data byte."""
        track_data = bytes(writeVar(0)) + bytes([0xF3, 0x05])
        collector = self._parse(track_data)
        ss_events = [e for e in collector.events if e[0] == 'song_select']
        self.assertEqual(len(ss_events), 1)
        self.assertEqual(ss_events[0][1], 0x05)

    def test_tuning_request(self):
        """Tuning Request (0xF6) should read 0 data bytes."""
        track_data = bytes(writeVar(0)) + bytes([0xF6])
        collector = self._parse(track_data)
        tr_events = [e for e in collector.events if e[0] == 'tuning_request']
        self.assertEqual(len(tr_events), 1)


# ---------------------------------------------------------------------------
# Fix 2: tuning_request() used chr() instead of list/int for event_slice
# ---------------------------------------------------------------------------

class TestTuningRequestOutput(unittest.TestCase):

    def test_tuning_request_writes_bytes(self):
        """tuning_request() should write a valid byte, not a string."""
        midi_out = MidiOutFile()
        midi_out.start_of_track()
        # This used to raise because chr() returns a str, not bytes/list
        midi_out.tuning_request()
        data = list(midi_out._current_track_buffer.read_all())
        # Should contain: varlen(0) + 0xF6
        self.assertIn(c.TUNING_REQUEST, data)


# ---------------------------------------------------------------------------
# Fix 3: midi_port() used MIDI_CH_PREFIX (0x20) instead of MIDI_PORT (0x21)
# ---------------------------------------------------------------------------

class TestMidiPort(unittest.TestCase):

    def test_midi_port_uses_correct_constant(self):
        """midi_port() should write meta event type 0x21, not 0x20."""
        midi_out = MidiOutFile()
        midi_out.start_of_track()
        midi_out.midi_port(4)
        midi_out.end_of_track()
        data = list(midi_out.read_all())
        # Find the meta event: 0xFF followed by the type byte
        # MTrk header is 8 bytes, then varlen(0), then 0xFF, type, len, value
        # Look for the sequence [0xFF, 0x21, 0x01, 4]
        found = False
        for i in range(len(data) - 3):
            if data[i] == 0xFF and data[i+1] == c.MIDI_PORT and data[i+2] == 1 and data[i+3] == 4:
                found = True
                break
        self.assertTrue(found, f"Expected meta event with type 0x21 (MIDI_PORT), got data: {data}")

    def test_midi_port_differs_from_ch_prefix(self):
        """midi_port and midi_ch_prefix should write different meta event types."""
        midi_port_out = MidiOutFile()
        midi_port_out.start_of_track()
        midi_port_out.midi_port(4)
        midi_port_out.end_of_track()

        midi_ch_out = MidiOutFile()
        midi_ch_out.start_of_track()
        midi_ch_out.midi_ch_prefix(4)
        midi_ch_out.end_of_track()

        port_data = list(midi_port_out.read_all())
        ch_data = list(midi_ch_out.read_all())
        # They should differ (0x21 vs 0x20)
        self.assertNotEqual(port_data, ch_data)


# ---------------------------------------------------------------------------
# Fix 4: pitch_bend range was 0-32639 instead of 0-16383
# ---------------------------------------------------------------------------

class TestPitchBendRange(unittest.TestCase):

    def test_max_valid_pitch_bend(self):
        """16383 (max 14-bit value) should be accepted."""
        events = MidiEvents()
        events.pitch_bend(0, 16383)  # should not raise

    def test_zero_pitch_bend(self):
        """0 should be accepted."""
        events = MidiEvents()
        events.pitch_bend(0, 0)  # should not raise

    def test_over_max_pitch_bend_rejected(self):
        """16384 and above should be rejected."""
        events = MidiEvents()
        with self.assertRaises(AssertionError):
            events.pitch_bend(0, 16384)

    def test_old_max_now_rejected(self):
        """32639 (the old incorrect max) should now be rejected."""
        events = MidiEvents()
        with self.assertRaises(AssertionError):
            events.pitch_bend(0, 32639)


# ---------------------------------------------------------------------------
# Fix 5: END_OFF_EXCLUSIVE renamed to END_OF_EXCLUSIVE
# ---------------------------------------------------------------------------

class TestEndOfExclusiveNaming(unittest.TestCase):

    def test_constant_exists(self):
        """END_OF_EXCLUSIVE should exist and equal 0xF7."""
        self.assertEqual(c.END_OF_EXCLUSIVE, 0xF7)

    def test_old_name_removed(self):
        """END_OFF_EXCLUSIVE should no longer exist."""
        self.assertFalse(hasattr(c, 'END_OFF_EXCLUSIVE'))

    def test_sysex_roundtrip_uses_correct_terminator(self):
        """Writing a sysex event should use END_OF_EXCLUSIVE (0xF7) as terminator."""
        midi_out = MidiOutFile()
        midi_out.start_of_track()
        midi_out.sysex_event(bytearray([0x41, 0x10, 0x42]))
        data = list(midi_out._current_track_buffer.read_all())
        self.assertIn(0xF7, data)


# ---------------------------------------------------------------------------
# Fix 6: README truncated line (tested indirectly via Transposer pattern)
# ---------------------------------------------------------------------------

class TestTransposerPattern(unittest.TestCase):

    def test_transposer_from_readme(self):
        """The Transposer pattern from the README should work correctly."""

        class Transposer(MidiOutFile):
            delta = 24

            def _transp(self, ch, note):
                if ch != 9:
                    if 0 <= (note + self.delta) <= 127:
                        note += self.delta
                return note

            def note_on(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
                note = self._transp(channel, note)
                MidiOutFile.note_on(self, channel, note, velocity, use_running_status)

            def note_off(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
                note = self._transp(channel, note)
                MidiOutFile.note_off(self, channel, note, velocity, use_running_status)

        midi_out = Transposer()
        midi_out.header(format=0, nTracks=1, division=96)
        midi_out.start_of_track()
        midi_out.update_time(0)
        midi_out.note_on(0, 40, 100)
        midi_out.update_time(96)
        midi_out.note_off(0, 40, 64)
        midi_out.update_time(0)
        midi_out.end_of_track()
        data = list(midi_out.read_all())
        # note 40 + delta 24 = 64, which is 0x40
        # Find note_on: status 0x90, note 64, velocity 100
        self.assertIn(64, data)  # transposed note should be present


# ---------------------------------------------------------------------------
# Fix 7: aftertouch parameter renamed from velocity to pressure
# ---------------------------------------------------------------------------

class TestAftertouchParameter(unittest.TestCase):

    def test_aftertouch_accepts_pressure_kwarg(self):
        """aftertouch() should accept 'pressure' keyword argument."""
        events = MidiEvents()
        events.aftertouch(channel=0, note=64, pressure=100)

    def test_aftertouch_rejects_over_range_pressure(self):
        """aftertouch() should reject pressure > 127."""
        events = MidiEvents()
        with self.assertRaises(AssertionError):
            events.aftertouch(channel=0, note=64, pressure=200)

    def test_aftertouch_output_uses_pressure(self):
        """MidiOutFile.aftertouch() should accept pressure kwarg and write correct bytes."""
        midi_out = MidiOutFile()
        midi_out.start_of_track()
        midi_out.aftertouch(channel=0, note=64, pressure=100)
        data = list(midi_out._current_track_buffer.read_all())
        # Should contain: varlen(0), status (0xA0 + 0), note (64), pressure (100)
        expected_status = (c.AFTERTOUCH << 4) + 0  # 0xA0
        self.assertIn(expected_status, data)
        # Find the sequence: status, note, pressure
        for i in range(len(data) - 2):
            if data[i] == expected_status and data[i+1] == 64 and data[i+2] == 100:
                break
        else:
            self.fail(f"Expected aftertouch event [0xA0, 64, 100] not found in {data}")


# Python's assert raises AssertionError (not AssertionError with a typo),
# but in this codebase the error messages use "AssertionError" in docstrings.
# The actual exception type is still AssertionError.
AssertionError = AssertionError


if __name__ == '__main__':
    unittest.main()
