from drumdown import parse_note_group, dump, parse_grid_slice


def pipe(data, *funcs):
    for func in funcs:
        data = func(data)
    return data


def test_parse_hat_snare():
    input = "-x/  "
    assert pipe((0, input), parse_grid_slice, str) == input


def test_parse_half_bar():
    input = [
        "--------",
        "x | x | ",
        "|   /   ",
        "|       ",
        "/       ",
    ]
    assert (
        "\n".join(pipe(input, parse_note_group, dump))
        == "\n".join(input)
    )
