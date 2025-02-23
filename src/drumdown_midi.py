import mido
import itertools

from typing import List
from .drumdown import GridSlice, Note


TD_17KVX_NOTES = {
    Note.CLOSED_HAT: 42,
    Note.KICK: 36,
    Note.SNARE: 38,
    Note.TOM: 41,
    Note.REST: None,
}
DEFAULT_TICKS_PER_BEAT = 480

NoteGroup = List[GridSlice]
Phrase = List[NoteGroup]
Song = List[Phrase]


def write_note_group_to_midi(
    track: mido.MidiTrack,
    note_group: NoteGroup,
    ticks_per_beat=DEFAULT_TICKS_PER_BEAT,
    offset=None,
):
    sixteenth_note_duration = ticks_per_beat // 4
    if offset is None:
        offset = -sixteenth_note_duration
    for i, grid_slice in enumerate(note_group):
        if grid_slice.is_rest:
            offset += sixteenth_note_duration
            continue
        sorted_notes = sorted(list(grid_slice.notes))
        for note_i, note in enumerate(sorted_notes):
            midi_note = TD_17KVX_NOTES[note]
            if midi_note:
                msg = mido.Message(
                    "note_on",
                    note=midi_note,
                    velocity=64,
                    time=(
                        offset + sixteenth_note_duration if note_i == 0 else 0
                    ),
                )
                track.append(msg)
        for note_i, note in enumerate(sorted_notes):
            midi_note = TD_17KVX_NOTES[note]
            if midi_note:
                msg = mido.Message(
                    "note_off",
                    note=midi_note,
                    velocity=64,
                    time=sixteenth_note_duration if note_i == 0 else 0,
                )
                track.append(msg)
                offset = -sixteenth_note_duration
    return offset


def write_phrase_to_midi(
    track: mido.MidiTrack,
    phrase: Phrase,
    ticks_per_beat=DEFAULT_TICKS_PER_BEAT,
    offset=None,
):
    offset = None
    for note_group in phrase:
        offset = write_note_group_to_midi(
            track, note_group, ticks_per_beat=ticks_per_beat, offset=offset
        )
    return offset


def write_song_to_midi(
    track: mido.MidiTrack,
    song: Song,
    ticks_per_beat=DEFAULT_TICKS_PER_BEAT,
):
    offset = None
    note_groups = list(itertools.chain.from_iterable(song))
    write_phrase_to_midi(track, note_groups, ticks_per_beat)
