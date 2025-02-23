from enum import Enum
from typing import List, Tuple, Set
from dataclasses import dataclass


class Note(Enum):
    CLOSED_HAT = "x"
    KICK = "K"
    REST = "|"
    SNARE = "s"
    TOM = "t"

    def __lt__(self, other):
        if isinstance(other, Note):
            return self.value < other.value
        return NotImplemented


NoteSet = Set[Note]


@dataclass
class GridSlice:
    note_type: str
    notes: NoteSet
    index: int

    @property
    def is_rest(self):
        return self.notes == {Note.REST}

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


NoteGroup = List[GridSlice]


@dataclass
class Heading:
    text: str
    depth: int


@dataclass
class Phrase:
    groups: List[NoteGroup]

    def __iter__(self):
        return iter(self.groups)


@dataclass
class Song:
    nodes: List[Phrase | Heading]

    @property
    def phrases(self) -> List[Phrase]:
        return [node for node in self.nodes if type(node) == Phrase]


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


def dump_note_group(x: List[GridSlice]) -> List[str]:
    return transpose(list(map(str, x)))


def parse_phrase(x: List[str]) -> Phrase:
    note_type_line = x[0]
    group_lengths = [len(x) for x in note_type_line.split()]
    tx = transpose(x)
    groups = []
    for l in group_lengths:
        groups.append(
            parse_note_group(transpose(tx[:l]))
        )
        tx = tx[l+2:]
    return Phrase(groups)


def concatenate_note_groups(x: List[str], y: List[str]) -> List[str]:
    if not x:
        return y
    return [a + b for a, b in zip(x, y)]


def dump_phrase(x: Phrase) -> List[str]:
    dumped_groups = [dump_note_group(group) for group in x]
    out: List[str] = []
    for i, g in enumerate(dumped_groups):
        out = concatenate_note_groups(out, g)
        if i < len(dumped_groups) - 1:
            out = concatenate_note_groups(out, ["  "] * len(g))
    return out
