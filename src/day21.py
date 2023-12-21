"""
Part 2 considerations

26501365 is N * 131 + 65, where 131 is the map height/width and 65 is half of that.
So after 26501365 steps, it will have traversed the half the original + N maps in any 
direction, because there's a straight line of 65 steps from S to all four edges. So
along any of the axes, 2N+1 gardens will be filled.

When entering from the side (any side), it takes 195 steps to visit every position, after
which the visited count in this map will only cycle between even and odd. Or maybe 196
steps if you include the initial step to enter the map.

After 131 steps in any direction, we reach the neighboring S. From there on, we can only
go (N-1)*131 + 65 tiles upwards or downwards, then (N-2)*131. I assume this means we span
some kind of diamond shape of filled maps somehow.

I thought a while about precomputing which garden has which parity, but only then thought
of the diamond shape and felt intimidated by the edges, which I'd also have to cover.
In the end, I gave up on figuring it out analytically and logged values corresponding to
      f(0*131 + 65) = y0
      f(1*131 + 65) = y1
      f(2*131 + 65) = y2
      f(3*131 + 65) = y3
      ...

because I had read a hint about people fitting a quadratic function. Playing around with
interpolations also confirmed for me that a quadratic fit worked best, which makes sense
in light of this covering a number of gardens that's quadratic in N. I actually fit the
pairs [(0, y0), (1, y1), (2, y2), (3, y3)], which give nice (almost) integer coefficients
and then apply it to f((26501365 - 65) / 131).

I was worried that the alternating even-odd parity of adjacent gardens would make the
fit not work, but somehow it does anyway. I'm not exacly sure why that is, I could have
imagined that I have to fit separate functions for (0, 2, 4) and (1, 3, 5). Oh well.
"""
import sys
from pprint import pprint

import numpy as np
from tqdm import tqdm

import utils

puzzle = [list(l) for l in utils.read_puzzle_input(sys.argv[1])]
h, w = utils.input_dim(puzzle)

start = [(i, j) for i in range(h) for j in range(w) if puzzle[i][j] == "S"][0]
positions = set({start})


def print_map(puzzle, past_positions):
    """Used during debugging & exploration."""
    print(
        "\n".join(
            [
                "".join(
                    c if (i, j) not in past_positions[step % 2] else "O"
                    for (j, c) in enumerate(l)
                )
                for i, l in enumerate(puzzle)
            ]
        )
    )


# Only for part 2 - part 1 is easy. I had some optimization for part 2
# not move old values redundantly (we know where they are, depending on
# even or odd steps), but I removed that to keep it simple and to ensure
# I don't mess up after I finally figured out the interpolation.
reached_log = []
N = h * 4 + h // 2
for step in tqdm(range(N)):
    next_positions = set()
    for i, j in positions:
        for di, dj in {(-1, 0), (1, 0), (0, 1), (0, -1)}:
            ni, nj = (i + di, j + dj)

            lookup_i = ni % h
            lookup_j = nj % w

            # Don't go across walls.
            if puzzle[lookup_i][lookup_j] == "#":
                continue

            next_positions.add((ni, nj))

    positions = next_positions

    # We reached the end of garden k*131 + 65.
    if ((step + 1) - h // 2) % h == 0:
        k = ((step + 1) - h // 2) // h
        reached_log.append((k, len(positions)))

x, y = zip(*reached_log)
coeffs = [round(c) for c in np.polyfit(x, y, deg=2)]

arg = (26501365 - 65) // 131
answer = coeffs[0] * arg**2 + coeffs[1] * arg + coeffs[0]
print(answer)
