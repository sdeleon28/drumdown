from typing import List, Tuple
from dataclasses import dataclass


CLOSED_HAT = "x"
KICK = "K"
REST = "|"
SNARE = "s"
TOM = "t"


@dataclass
class GridSlice:
    notes: set
    index: int

    def __str__(self):
        hat = "|" if self.index % 2 == 0 else " "
        if CLOSED_HAT in self.notes:
            hat = "x"
        snare = " "
        if SNARE in self.notes:
            snare = "/"
        elif KICK in self.notes:
            snare = "|"
        tom = " "
        if TOM in self.notes:
            tom = "/"
        elif KICK in self.notes:
            tom = "|"
        kick = " "
        if KICK in self.notes:
            kick = "/"
        return "".join([
            "-",
            hat,
            snare,
            tom,
            kick,
        ])


def transpose(x: List[str]) -> List[str]:
    return [''.join(i) for i in zip(*x)]


def parse_grid_slice(i_x: Tuple[int, str]) -> GridSlice:
    i, x = i_x
    if x == "-x||/":
        return GridSlice({ CLOSED_HAT, KICK }, i)
    elif x == "-x/  ":
        return GridSlice({ CLOSED_HAT, SNARE }, i)
    else:
        return GridSlice({ REST }, i)


def parse_note_group(x: List[str]) -> List[GridSlice]:
    return list(map(parse_grid_slice, enumerate(transpose(x))))


def dump(x: List[GridSlice]) -> List[str]:
    return transpose(list(map(str, x)))
