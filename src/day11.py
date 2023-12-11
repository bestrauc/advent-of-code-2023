import itertools
import sys

import utils

puzzle_input = utils.read_puzzle_input(sys.argv[1])
h, w = utils.input_dim(puzzle_input)

factor = 1000000    # factor = 2 for Part 1

row_expansions = [(factor - 1) * (set(l) == {"."}) for l in puzzle_input]
row_expansions = list(itertools.accumulate(row_expansions))

col_expansions = [
    (factor - 1) * ({puzzle_input[i][j] for i in range(h)} == {"."})
    for j in range(w)
]
col_expansions = list(itertools.accumulate(col_expansions))

galaxies = [
    (i + row_expansions[i], j + col_expansions[j])
    for i, row in enumerate(puzzle_input)
    for j, c in enumerate(row)
    if c == "#"
]

# Compute pairwise manhattan distance.
acc = 0
for (i, gal1) in enumerate(galaxies):
    for (j, gal2) in enumerate(galaxies[i:]):
        (g1_y, g1_x) = gal1
        (g2_y, g2_x) = gal2

        dist = abs(g2_x - g1_x) + abs(g2_y - g1_y)
        acc += dist

        # print(f"{i+1} -> {i+j+1} = {dist}")

print(acc)
