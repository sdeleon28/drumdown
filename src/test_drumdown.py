import os

from typing import List
from .drumdown import (
    GridSlice,
    Note,
    dump_phrase,
    dump_song,
    parse_note_group,
    dump_note_group,
    parse_grid_slice,
    parse_phrase,
    parse_song,
)


def pipe(data, *funcs):
    for func in funcs:
        data = func(data)
    return data


def test_parse_money_beat_half_bar():
    input = [
        "--------",
        "x x x x ",
        "|   /   ",
        "|       ",
        "/       ",
    ]
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
    assert parse_note_group(input) == half_money_beat


def test_parse_money_beat_half_bar_and_dump_it():
    input = [
        "--------",
        "x | x | ",
        "|   /   ",
        "|       ",
        "/       ",
    ]
    assert pipe(
        input, parse_note_group, dump_note_group, "\n".join
    ) == "\n".join(input)


def test_parse_busier_kick_pattern_and_dump_it():
    input = [
        "--------",
        "x | x | ",
        "| | / | ",
        "| |   | ",
        "/ /   / ",
    ]
    assert pipe(
        input, parse_note_group, dump_note_group, "\n".join
    ) == "\n".join(input)


def test_parse_sixteenth_roll_and_dump_it():
    input = [
        "3e+a4e+a",
        "|  || ||",
        "|  // //",
        "/       ",
        "/       ",
    ]
    assert pipe(
        input, parse_note_group, dump_note_group, "\n".join
    ) == "\n".join(input)


def remove_empty_lines(x):
    return filter(bool, x)


def test_parse_phrase_and_dump_it():
    input = [
        "--------  --------  3e+a4e+a  3e+a4e+a",
        "x | x |   x | x |   |  || ||  |  || ||",
        "|   /     |   /     |  // //  |  // //",
        "|         |         /         /       ",
        "/         /         /         /       ",
    ]
    assert pipe(
        input,
        parse_phrase,
        dump_phrase,
        remove_empty_lines,
        "\n".join,
    ) == "\n".join(input)


def test_parse_phrase_with_loop_and_dump_it():
    input = [
        "--------  --------  3e+a4e+a  3e+a4e+a  |   ",
        "x | x |   x | x |   |  || ||  |  || ||  |   ",
        "|   /     |   /     |  // //  |  // //  |   ",
        "|         |         /         /         |   ",
        "/         /         /         /         | x3",
    ]
    assert pipe(
        input,
        parse_phrase,
        dump_phrase,
        remove_empty_lines,
        "\n".join,
    ) == "\n".join(input)


def test_parse_heading_and_phrase_and_dump_it():
    input = [
        "# verse 1",
        "",
        "--------  --------  3e+a4e+a  3e+a4e+a",
        "x | x |   x | x |   |  || ||  |  || ||",
        "|   /     |   /     |  // //  |  // //",
        "|         |         /         /       ",
        "/         /         /         /       ",
        "",
        "",
    ]
    assert pipe(input, parse_song, dump_song, "\n".join) == "\n".join(input)


def test_parse_song_with_more_note_types_and_dump_it():
    input = [
        "# verse 1",
        "",
        "--------  --------  --------  ----====",
        "x | x |   x | | C   | | | |   | | ||||",
        "|   /     | | / |     | /     | | / **",
        "|         | |   |     |       / | /   ",
        "/         / /   /     /       / /     ",
        "",
        "",
        "# chorus 1",
        "",
        "--------  --------  --------  --------",
        "C | r r   r r r r   r r r r   r r r r ",
        "|   /     | | /     |   /     | | /   ",
        "|         | |       |         | |     ",
        "/         / /       /         / /     ",
        "",
        "",
        "--------  --------  --------  --------",
        "r r r r   r r o -   } | | |   | | | | ",
        "|   /     | | /     |                 ",
        "|         | |       |                 ",
        "/         / /       /                 ",
        "",
        "",
    ]
    assert pipe(input, parse_song, dump_song, "\n".join) == "\n".join(input)


def test_parse_full_song():
    examples_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "examples/"
    )
    # TODO:
    # for example in os.listdir(examples_dir):
    for example in ["test.drumdown"]:
        filename = os.path.join(examples_dir, example)
        with open(filename, "r") as f:
            lines = [line.replace("\n", "") for line in f.readlines()]
            assert (
                pipe(
                    lines,
                    parse_song,
                    dump_song,
                    lambda data: map(lambda x: x.strip(), data),
                    list
                )
                == [line.strip() for line in lines]
            )
