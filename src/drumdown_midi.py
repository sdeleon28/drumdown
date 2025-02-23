import mido

from typing import List
from src.drumdown import GridSlice, Note


TD_17KVX_NOTES = {
    Note.CLOSED_HAT: 42,
    Note.KICK: 36,
    Note.SNARE: 38,
    Note.TOM: 41,
    Note.REST: None,
}


def write_note_group_to_midi(
    track: mido.MidiTrack,
    note_group: List[GridSlice],
    ticks_per_beat=480,
    offset=None,
):
    sixteenth_note_duration = ticks_per_beat // 4
    if offset is None:
        offset=-sixteenth_note_duration
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
