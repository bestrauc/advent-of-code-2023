import sys
import re
import math

puzzle_input = [l.strip() for l in open(sys.argv[1]).readlines()]

# Parse the part numbers in a first iteration over the input.
number_intervals = {
        i: [(m.span(), int(m.group())) for m in re.finditer("(\d+)", line)]
        for i,line in enumerate(puzzle_input)
    }

def neighboring_intervals(i: int, j: int, number_intervals: dict[list]) -> set[int]:
    """Check the neighborhood of (i, j) for part numbers."""

    neighbors = set()
    for di in [-1, 0, +1]:
        for dj in [-1, 0, +1]:
            if (di == 0) and (dj == 0):
                continue

            # Handle out of bounds or lines without any part numbers with .get
            line_intervals = number_intervals.get(i+di, [])
            matching = matching_interval(j+dj, line_intervals)

            if matching is not None:
                neighbors.add(matching)

    return neighbors

def matching_interval(j: int, line_intervals: list) -> int | None:
    for (int_s, int_e), number in line_intervals:
        if int_s <= j < int_e:
            return number

    return None

def get_part_nums_for_all_symbols(puzzle_input: list[list]):
    symbol_part_numbers = {}
    for i, line in enumerate(puzzle_input):
        for j, c in enumerate(line):
            if c.isdigit() or c == ".":
                continue

            neighbor_parts = neighboring_intervals(i, j, number_intervals) 
            if len(neighbor_parts) > 0:
                # Save coordinate and symbol just in case (ha, part2!)
                symbol_part_numbers[(i, j, c)] = neighbor_parts

    return symbol_part_numbers

symbol_part_nums = get_part_nums_for_all_symbols(puzzle_input)

# Part 1
part_number_sum = sum(sum(parts) for parts in symbol_part_nums.values())
print(part_number_sum)

# Part 2
gear_ratio_sum = sum(
    math.prod(parts) 
    for (_i, _j, symbol), parts in symbol_part_nums.items()
    if symbol == "*" and len(parts) == 2
)

print(gear_ratio_sum)
