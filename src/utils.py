import re

def split_list_at(l: list, pat: str) -> list[list]:
    try:
        idx = l.index(pat)
    except ValueError:
        return [l]

    return [l[:idx]] + split_list_at(l[idx + 1 :], pat)

def read_puzzle_input(input_path: str) -> list[str]:
    return [l.strip() for l in open(input_path).readlines()]


def nums(line: str) -> list[int]:
    return [int(n) for n in re.findall(r"(-*\d+)", line)]

def input_dim(inp: list[str]) -> tuple[int, int]:
    """Return (height, width) of a 2D input."""
    return len(inp), len(inp[0])

def transpose(l: list[list]) -> list[list]:
    return list(map(list, zip(*l)))
