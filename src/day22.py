import functools
import sys
from collections import defaultdict

import numpy as np
from tqdm import tqdm

import utils


def get_brick_coords(line: str) -> np.array:
    return [list(map(int, pos.split(","))) for pos in line.split("~")]


puzzle = utils.read_puzzle_input(sys.argv[1])
bricks = [get_brick_coords(line) for line in puzzle]

# Sort the bricks by (z, x, y) coordinates, so the lowest are first.
bricks = sorted(bricks, key=lambda b: (b[0][2], b[0][0], b[0][1]))


def dimrange(b: list, dim: int) -> tuple[int, int]:
    return min(b[0][dim], b[1][dim]), max(b[0][dim], b[1][dim])


def overlaps(range1: tuple, range2: tuple) -> bool:
    return max(range1[0], range2[0]) <= min(range1[1], range2[1])


def can_drop(b: list, bricks_below: list) -> list:
    b_xrange = dimrange(b, dim=0)
    b_yrange = dimrange(b, dim=1)

    colliding_bricks_below = [
        (i, bi)
        for i, bi in bricks_below
        if overlaps(b_xrange, dimrange(bi, dim=0))
        and overlaps(b_yrange, dimrange(bi, dim=1))
    ]

    return colliding_bricks_below


def without_key(d: dict, key) -> dict:
    return {k: v for k, v in d.items() if k != key}


def main():
    # To not have to search all bricks in the z-direction later, retain a
    # small look-up table to quickly get the bricks at a given height.
    bricks_per_height = defaultdict(set)
    for i, b in enumerate(bricks):
        b_zrange = dimrange(b, dim=2)
        bricks_per_height[b_zrange[1]].add(i)

    # When a brick has settled, we save on which other bricks it has settled on.
    supporting = {i: set() for i in range(len(bricks))}
    for i in tqdm(range(len(bricks))):
        # We drop a single brick layer by layer, checking for obstructions
        # in the x-y plane at each step. A smart data structure could probably
        # drop it all the way at once.
        while True:
            bricks_below = [
                (b, bricks[b]) for b in bricks_per_height[bricks[i][0][2] - 1]
            ]
            colliding_below = can_drop(bricks[i], bricks_below)

            # Stop when we can't drop further (at bottom or an obstruction).
            if len(colliding_below) > 0 or (dimrange(bricks[i], dim=2)[0] == 1):
                break

            # We can decrease the z-coordinate.
            bricks[i][0][2] -= 1
            bricks[i][1][2] -= 1

            # Update our index of which z-plane the top of the bricks lie in.
            old_height = bricks[i][1][2] + 1
            new_height = bricks[i][1][2]

            bricks_per_height[old_height] -= {i}
            bricks_per_height[new_height] |= {i}

        for bi, _ in colliding_below:
            supporting[bi].add(i)

    acc = 0
    for k, v in supporting.items():
        without = set().union(*without_key(supporting, k).values())
        if v <= without:
            acc += 1

    print(acc)

    # Also create the inverse map (what bricks a brick rests on) for part 2.
    supported_by = defaultdict(set)
    for b, supps in supporting.items():
        for sup_b in supps:
            supported_by[sup_b].add(b)

    def chain_reaction(bi: int) -> set:
        """Awkward recursion where I mutate a dictionary to remove the supports.

        Can probably be formulated in a nicer way that's amenable to memoization.
        """
        remaining_supported_by = {k: v.copy() for k, v in supported_by.items()}

        def f(bi):
            for b in remaining_supported_by.keys():
                remaining_supported_by[b] -= {bi}

            for b in supporting[bi]:
                if len(remaining_supported_by[b]) == 0:
                    f(b)

        f(bi)
        return len([v for v in remaining_supported_by.values() if len(v) == 0])

    # Unfortunately kind of slow - not an ideal solution in any case.
    print(sum(chain_reaction(bi) for bi in tqdm(range(len(bricks)))))


main()
