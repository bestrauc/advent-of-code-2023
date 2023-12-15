import copy
import sys
from collections import defaultdict

import utils


def print_platform(l: list[list[str]]):
    print("\n".join(["".join(row) for row in l]))


def rotate(platform: list[list[str]]):
    """Rotate a 2D matrix 90 degrees counterclockwise."""
    return utils.transpose(platform[::-1])


def move_north(platform: list[list[str]]):
    """Move all rocks north. For other directions, we rotate the platform."""
    platform = copy.deepcopy(platform)
    free_row_above = dict()
    for i, row in enumerate(platform):
        for j in range(len(row)):
            if platform[i][j] == "O" and (free_row_above.get(j) is not None):
                platform[free_row_above[j]][j] = platform[i][j]
                platform[i][j] = "."

                # The space above the insert position is now the highest free one.
                free_row_above[j] += 1

            if platform[i][j] == "." and (free_row_above.get(j) is None):
                free_row_above[j] = i
            elif platform[i][j] in set("O#"):
                free_row_above[j] = None

    return platform


def move_cycle(platform: list[list[str]]) -> list[list[str]]:
    for i in range(4):
        platform = move_north(platform)
        platform = rotate(platform)

    return platform


def compute_load(platform: list[list[str]]) -> int:
    return sum(
        [
            len(platform) - i
            for i, row in enumerate(platform)
            for j, c in enumerate(row)
            if c == "O"
        ]
    )


def hash_platform(platform: list[list[str]]) -> int:
    return hash(tuple(map(tuple, platform)))


platform = [list(l) for l in utils.read_puzzle_input(sys.argv[1])]

# Part 1
print(compute_load(move_north(platform)))

# Part 2
previous_states = {}  # track board states.

cycle_len = None
cycle_prefix = None
for i in range(100000000):
    platform_hash = hash_platform(platform)

    # If we encounter a platform configuration again, we've seen them all.
    # From here on out, a sequence of states will repeat in a certain cycle.
    if platform_hash in previous_states:
        cycle_len = i - previous_states[platform_hash][0]
        cycle_prefix = previous_states[platform_hash][0]
        break

    previous_states[platform_hash] = (i, platform)
    platform = move_cycle(platform)

states_by_time = dict(previous_states.values())

# We've entered a cycle after a certain number of steps.
state_at_end = (1000000000 - cycle_prefix) % cycle_len + cycle_prefix
print(compute_load(states_by_time[state_at_end]))
