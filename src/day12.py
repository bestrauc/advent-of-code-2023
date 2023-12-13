import functools
import sys

import utils

puzzle_input = utils.read_puzzle_input(sys.argv[1])
springs_and_counts = [p.split() for p in puzzle_input]


@functools.cache
def count_combinations(springs: str, groups: tuple[int]) -> int:
    """Recursively consume the string and cache repeated subproblems."""

    # If we've exhausted all groups, that is fine unless there are
    # springs left to cover, which would make it an invalid solution.
    if len(groups) == 0:
        return int("#" not in springs)

    # If there aren't enough springs left for the next group,
    # this is also an invalid solution and we don't count it.
    group_len = groups[0]
    if len(springs) < group_len:
        return 0

    group = springs[:group_len]
    insert_possible = set(group) <= set("#?")
    space_after_group = (springs + ".")[group_len] in "?."

    # If we are at a "#", we _have_ to start the group here.
    if springs[0] == "#":
        # If we can't start a group despite having to, we won't find
        # any valid combinations in this recursion branch and can stop.
        if not (insert_possible and space_after_group):
            return 0

        return count_combinations(springs[group_len + 1 :], groups[1:])
    # If we are at a "?", we _may_ start a group here.
    elif springs[0] == "?" and insert_possible and space_after_group:
        # If we inserted the ###.. here and need to leave a space after.
        group_used = count_combinations(springs[group_len + 1 :], groups[1:])
        # If we chose not to do it, we just skip along.
        no_group = count_combinations(springs[1:], groups)

        return group_used + no_group
    # Otherwise, we can't start a group here at all.
    else:
        return count_combinations(springs[1:], groups)


acc_part1 = 0
acc_part2 = 0

for (springs, counts), p in zip(springs_and_counts, puzzle_input):
    counts1 = tuple(map(int, counts.split(",")))
    acc_part1 += count_combinations(springs, counts1)

    springs2 = "?".join([springs] * 5)
    counts2 = tuple(map(int, (",".join([counts] * 5)).split(",")))
    acc_part2 += count_combinations(springs2, counts2)

print(acc_part1, acc_part2)
