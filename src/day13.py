import sys
from pprint import pprint
from typing import Iterator

import utils

puzzle_input = list(map(list, utils.read_puzzle_input(sys.argv[1])))


def split_list_at(l: list, pat: str) -> list[list]:
    try:
        idx = l.index(pat)
    except ValueError:
        return [l]

    return [l[:idx]] + split_list_at(l[idx + 1 :], pat)


def reflects(row: str, reflect_idx: int) -> bool:
    """Check if a string has a reflection at the given position.
    
    e.g. abaababc, reflect_idx=2 -> True, because aba|aba..
    """
    left = row[:reflect_idx]
    right = row[reflect_idx:]

    refl_len = min(len(left), len(right))
    return left[-refl_len:] == right[:refl_len][::-1]


def reflect_idxs(row: str) -> set[int]:
    """Get all positions that can create a reflection."""
    return {i for i in range(1, len(row)) if reflects(row, i)}


def pattern_reflection(pattern: list[str], prev: int = None) -> int | None:
    """Search for reflections in each row and return the common one, if any."""
    candidates = set(range(len(pattern[0]))) - {prev or -1}
    for row in pattern:
        candidates &= reflect_idxs(row)

    if len(candidates) == 0:
        return None

    assert len(candidates) == 1
    return candidates.pop()


def unsmuged_reflection_gen(pattern: list[str]) -> Iterator[list[str]]:
    """Replace all # and .'s with their opposites and yield the variantions."""
    for (i, row) in enumerate(pattern[::]):
        for (j, c) in enumerate(row):
            pattern[i][j] = "." if c == "#" else "#"
            yield pattern
            pattern[i][j] = c


patterns = split_list_at(puzzle_input, pat=[])

# Part 1 is straightforward.
vert_acc = 0
hori_acc = 0
existing_refls = {}
for (i, pattern) in enumerate(patterns):
    if vert_refl := pattern_reflection(pattern):
        existing_refls[i] = (vert_refl, None)
        vert_acc += vert_refl
    elif hori_refl := pattern_reflection(utils.transpose(pattern)):
        existing_refls[i] = (None, hori_refl)
        hori_acc += hori_refl
    else:
        raise AssertionError("One reflection should exist")

print(vert_acc + hori_acc * 100)

# Part 2 has a separate loop over all the de-smudged pattern variations
# and ignores reflection positions that were found on the smudged version.
vert_acc = 0
hori_acc = 0
for (i, pattern) in enumerate(patterns):
    (prev_vert_refl, prev_hori_refl) = existing_refls[i]
    for pattern_variant in unsmuged_reflection_gen(pattern):
        if vert_refl := pattern_reflection(pattern_variant, prev=prev_vert_refl):
            vert_acc += vert_refl
            break
        elif hori_refl := pattern_reflection(utils.transpose(pattern_variant), prev=prev_hori_refl):
            hori_acc += hori_refl
            break
        else:
            # Here no reflection necessarily needs to exist.
            pass
    else:
        raise AssertionError("No new reflection found for any smudge")

print(vert_acc + hori_acc * 100)
