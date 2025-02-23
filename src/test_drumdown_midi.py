import mido

from typing import List, Tuple
from src.drumdown import GridSlice, Note
from src.drumdown_midi import write_note_group_to_midi

half_money_beat = [
    GridSlice("-", {Note.KICK, Note.CLOSED_HAT}, 0),
    GridSlice("-", {Note.REST}, 1),
    GridSlice("-", {Note.CLOSED_HAT}, 2),
    GridSlice("-", {Note.REST}, 3),
    GridSlice("-", {Note.CLOSED_HAT, Note.SNARE}, 4),
    GridSlice("-", {Note.REST}, 5),
    GridSlice("-", {Note.CLOSED_HAT}, 6),
    GridSlice("-", {Note.REST}, 7),
]


def test_write_note_group_to_midi():
    filename = "test.mid"

    ticks_per_beat = 4
    out_mid = mido.MidiFile(ticks_per_beat=ticks_per_beat)
    track = mido.MidiTrack()
    out_mid.tracks.append(track)
    write_note_group_to_midi(track, half_money_beat, ticks_per_beat=ticks_per_beat)
    out_mid.save(filename)

    read_mid = mido.MidiFile(filename)
    assert len(read_mid.tracks) == 1
    ticks_per_beat = read_mid.ticks_per_beat

    assert read_mid.tracks[0] == mido.MidiTrack(
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


def test_write_multiple_note_groups_to_midi():
    filename = "test.mid"

    ticks_per_beat = 4
    out_mid = mido.MidiFile(ticks_per_beat=ticks_per_beat)
    track = mido.MidiTrack()
    out_mid.tracks.append(track)
    offset = write_note_group_to_midi(track, half_money_beat, ticks_per_beat=ticks_per_beat)
    write_note_group_to_midi(track, half_money_beat, ticks_per_beat=ticks_per_beat, offset=offset)
    out_mid.save(filename)

    read_mid = mido.MidiFile(filename)
    assert len(read_mid.tracks) == 1
    ticks_per_beat = read_mid.ticks_per_beat

    assert read_mid.tracks[0] == mido.MidiTrack(
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

            mido.Message("note_on", channel=0, note=36, velocity=64, time=1),
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
