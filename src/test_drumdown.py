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
        "x | x | ",
        "|   /   ",
        "|       ",
        "/       ",
    ]
    assert pipe(
        input, parse_note_group, dump_note_group, "\n".join
    ) == "\n".join(input)


def test_parse_busier_kick_pattern():
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


def test_parse_sixteenth_roll():
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


def test_parse_phrase():
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


def test_parse_phrase_with_loop():
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


def test_parse_heading_and_phrase():
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


def test_parse_song_with_more_note_types():
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
