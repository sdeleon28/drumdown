import os
import mido

from typing import List, Tuple
from .drumdown import GridSlice, Heading, Note, Phrase, Song, parse_song
from .drumdown_midi import (
    write_note_group_to_midi,
    write_phrase_to_midi,
    write_song_to_midi,
)

half_money_beat = [
    GridSlice("-", {Note.KICK, Note.CLOSED_HAT}, 0),
    GridSlice("-", set([]), 1),
    GridSlice("-", {Note.CLOSED_HAT}, 2),
    GridSlice("-", set([]), 3),
    GridSlice("-", {Note.CLOSED_HAT, Note.SNARE}, 4),
    GridSlice("-", set([]), 5),
    GridSlice("-", {Note.CLOSED_HAT}, 6),
    GridSlice("-", set([]), 7),
]


def test_write_note_group_to_midi():
    filename = "test.mid"

    ticks_per_beat = 4
    out_mid = mido.MidiFile(ticks_per_beat=ticks_per_beat)
    track = mido.MidiTrack()
    out_mid.tracks.append(track)
    write_note_group_to_midi(
        track, half_money_beat, ticks_per_beat=ticks_per_beat
    )
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


def test_write_phrase_to_midi():
    filename = "test.mid"

    ticks_per_beat = 4
    out_mid = mido.MidiFile(ticks_per_beat=ticks_per_beat)
    track = mido.MidiTrack()
    out_mid.tracks.append(track)
    write_phrase_to_midi(
        track,
        Phrase([half_money_beat, half_money_beat], times=1),
        ticks_per_beat=ticks_per_beat,
    )
    out_mid.save(filename)

    read_mid = mido.MidiFile(filename)
    assert len(read_mid.tracks) == 1
    ticks_per_beat = read_mid.ticks_per_beat

    kick = 36
    hat = 42
    snare = 38
    assert read_mid.tracks[0] == mido.MidiTrack(
        [
            # group 1
            mido.Message("note_on", channel=0, note=kick, velocity=64, time=0),
            mido.Message("note_on", channel=0, note=hat, velocity=64, time=0),
            mido.Message("note_off", channel=0, note=kick, velocity=64, time=1),
            mido.Message("note_off", channel=0, note=hat, velocity=64, time=0),
            mido.Message("note_on", channel=0, note=hat, velocity=64, time=1),
            mido.Message("note_off", channel=0, note=hat, velocity=64, time=1),
            mido.Message("note_on", channel=0, note=snare, velocity=64, time=1),
            mido.Message("note_on", channel=0, note=hat, velocity=64, time=0),
            mido.Message("note_off", channel=0, note=snare, velocity=64, time=1),
            mido.Message("note_off", channel=0, note=hat, velocity=64, time=0),
            mido.Message("note_on", channel=0, note=hat, velocity=64, time=1),
            mido.Message("note_off", channel=0, note=hat, velocity=64, time=1),
            # group 1
            mido.Message("note_on", channel=0, note=kick, velocity=64, time=1),
            mido.Message("note_on", channel=0, note=hat, velocity=64, time=0),
            mido.Message("note_off", channel=0, note=kick, velocity=64, time=1),
            mido.Message("note_off", channel=0, note=hat, velocity=64, time=0),
            mido.Message("note_on", channel=0, note=hat, velocity=64, time=1),
            mido.Message("note_off", channel=0, note=hat, velocity=64, time=1),
            mido.Message("note_on", channel=0, note=snare, velocity=64, time=1),
            mido.Message("note_on", channel=0, note=hat, velocity=64, time=0),
            mido.Message("note_off", channel=0, note=snare, velocity=64, time=1),
            mido.Message("note_off", channel=0, note=hat, velocity=64, time=0),
            mido.Message("note_on", channel=0, note=hat, velocity=64, time=1),
            mido.Message("note_off", channel=0, note=hat, velocity=64, time=1),
            mido.MetaMessage("end_of_track", time=0),
        ]
    )


def test_write_song_to_midi():
    filename = "test.mid"

    ticks_per_beat = 4
    out_mid = mido.MidiFile(ticks_per_beat=ticks_per_beat)
    track = mido.MidiTrack()
    out_mid.tracks.append(track)
    write_song_to_midi(
        track,
        Song(
            [
                Heading("Money beat song", 1),
                Heading("Verse", 2),
                Phrase([half_money_beat, half_money_beat], times=1),
                Heading("Chorus", 2),
                Phrase([half_money_beat, half_money_beat], times=1),
            ]
        ),
        ticks_per_beat=ticks_per_beat,
    )
    out_mid.save(filename)

    read_mid = mido.MidiFile(filename)
    assert len(read_mid.tracks) == 1
    ticks_per_beat = read_mid.ticks_per_beat

    assert read_mid.tracks[0] == mido.MidiTrack(
        [
            # phrase 1
            # group 1
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
            # group 2
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
            # phrase 2
            # group 1
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
            # group 2
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


def test_parse_full_song_and_write_to_midi_file():
    midi_filename = "test.mid"
    ticks_per_beat = 4
    out_mid = mido.MidiFile(ticks_per_beat=ticks_per_beat)
    track = mido.MidiTrack()
    out_mid.tracks.append(track)

    examples_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "examples/"
    )
    example = "test.drumdown"
    example_filename = os.path.join(examples_dir, example)
    with open(example_filename, "r") as f:
        lines = [line.replace("\n", "") for line in f.readlines()]
        song = parse_song(lines)
        write_song_to_midi(track, song, ticks_per_beat=ticks_per_beat)
    out_mid.save(midi_filename)
