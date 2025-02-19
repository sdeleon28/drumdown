from enum import Enum
from typing import List, Tuple, Set
from dataclasses import dataclass


class Note(Enum):
    CLOSED_HAT = "x"
    KICK = "K"
    REST = "|"
    SNARE = "s"
    TOM = "t"


NoteSet = Set[Note]


@dataclass
class GridSlice:
    note_type: str
    notes: NoteSet
    index: int

    def __str__(self):
        hat = "|" if self.notes & {Note.REST, Note.SNARE, Note.KICK} else " "
        if Note.CLOSED_HAT in self.notes:
            hat = "x"
        snare = " "
        if Note.SNARE in self.notes:
            snare = "/"
        elif Note.KICK in self.notes:
            snare = "|"
        tom = " "
        if Note.TOM in self.notes:
            tom = "/"
        elif Note.KICK in self.notes:
            tom = "|"
        kick = " "
        if Note.KICK in self.notes:
            kick = "/"
        return "".join(
            [
                self.note_type,
                hat,
                snare,
                tom,
                kick,
            ]
        )


def transpose(x: List[str]) -> List[str]:
    return ["".join(i) for i in zip(*x)]


def parse_grid_slice(i_x: Tuple[int, str]) -> GridSlice:
    i, x = i_x
    notes: NoteSet = set([])
    note_type, hat, snare, tom, kick = list(x)
    match hat:
        case "x":
            notes.add(Note.CLOSED_HAT)
        case "|":
            notes.add(Note.REST)
    if tom == "/":
        notes.add(Note.TOM)
    if snare == "/":
        notes.add(Note.SNARE)
    if kick == "/":
        notes.add(Note.KICK)
    return GridSlice(note_type, notes, i)


def parse_note_group(x: List[str]) -> List[GridSlice]:
    return list(map(parse_grid_slice, enumerate(transpose(x))))


def dump(x: List[GridSlice]) -> List[str]:
    return transpose(list(map(str, x)))
