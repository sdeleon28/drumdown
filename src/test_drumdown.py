from typing import List
from .drumdown import GridSlice, Note, parse_note_group, dump, parse_grid_slice


def pipe(data, *funcs):
    for func in funcs:
        data = func(data)
    return data


def test_parse_money_beat_half_bar():
    input = [
        "--------",
        "x | x | ",
        "|   /   ",
        "|       ",
        "/       ",
    ]
    assert pipe(input, parse_note_group, dump, "\n".join) == "\n".join(input)


def test_parse_busier_kick_pattern():
    input = [
        "--------",
        "x | x | ",
        "| | / | ",
        "| |   | ",
        "/ /   / ",
    ]
    assert pipe(input, parse_note_group, dump, "\n".join) == "\n".join(input)


def test_parse_sixteenth_roll():
    input = [
        "3e+a4e+a",
        "|  || ||",
        "|  // //",
        "/       ",
        "/       ",
    ]
    assert pipe(input, parse_note_group, dump, "\n".join) == "\n".join(input)
