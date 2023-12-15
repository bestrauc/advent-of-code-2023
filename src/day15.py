import functools
import sys
from collections import defaultdict

import utils


def holiday_hash(s: str) -> int:
    return functools.reduce(lambda acc, c: (acc + ord(c)) * 17 % 256, s, 0)


puzzle_input = utils.read_puzzle_input(sys.argv[1])[0].split(",")
print(sum(map(holiday_hash, puzzle_input)))

# Rely on the fact that dict in Python maintains the insert order.
boxes = defaultdict(dict)
for elem in puzzle_input:
    if "=" in elem:
        label, focal = elem.split("=")
        box_idx = holiday_hash(label)
        boxes[box_idx][label] = int(focal)
    else:
        label = elem[:-1]
        box_idx = holiday_hash(label)
        boxes[box_idx].pop(label, None)


focusing_power = sum(
    sum(
        ((1 + box_idx) * (1 + slot_idx) * l)
        for slot_idx, l in enumerate(lenses.values())
    )
    for box_idx, lenses in boxes.items()
)
print(focusing_power)
