import mido

from typing import List, Tuple
from src.drumdown import GridSlice, Note
from src.drumdown_midi import TD_17KVX_NOTES, write_note_group_to_midi


def test_write_note_group_to_midi():
    note_group = [
        GridSlice("-", {Note.KICK, Note.CLOSED_HAT}, 0),
        GridSlice("-", {Note.REST}, 1),
        GridSlice("-", {Note.CLOSED_HAT}, 2),
        GridSlice("-", {Note.REST}, 3),
        GridSlice("-", {Note.CLOSED_HAT, Note.SNARE}, 4),
        GridSlice("-", {Note.REST}, 5),
        GridSlice("-", {Note.CLOSED_HAT}, 6),
        GridSlice("-", {Note.REST}, 7),
    ]

    filename = "test.mid"
    write_note_group_to_midi(note_group, filename, ticks_per_beat=4)
    mid = mido.MidiFile(filename, ticks_per_beat=16)
    assert len(mid.tracks) == 1
    ticks_per_beat = mid.ticks_per_beat

    expected_track = mido.MidiTrack(
        [
            mido.Message("note_on", channel=0, note=36, velocity=64, time=0),
            mido.Message("note_on", channel=0, note=42, velocity=64, time=0),
            mido.Message("note_off", channel=0, note=36, velocity=64, time=1),
            mido.Message("note_off", channel=0, note=42, velocity=64, time=0),
            mido.Message("note_on", channel=0, note=42, velocity=64, time=1),
            mido.Message("note_off", channel=0, note=42, velocity=64, time=1),
            mido.Message("note_on", channel=0, note=38, velocity=64, time=1),
            mido.Message("note_on", channel=0, note=42, velocity=64, time=0),
            mido.Message("note_off", channel=0, note=38, velocity=64, time=1),
            mido.Message("note_off", channel=0, note=42, velocity=64, time=0),
            mido.Message("note_on", channel=0, note=42, velocity=64, time=1),
            mido.Message("note_off", channel=0, note=42, velocity=64, time=1),
            mido.MetaMessage("end_of_track", time=0),
        ]
    )

    assert mid.tracks[0] == expected_track
