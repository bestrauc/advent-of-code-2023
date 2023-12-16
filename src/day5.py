import itertools
import sys
from dataclasses import dataclass, field

from tqdm import tqdm

import utils


@dataclass
class RangeMap:
    """Map a range as described in the task.

    Maps [source, source_end) -> [target, target_end)
    """

    source: int
    target: int
    size: int

    def __getitem__(self, key: int) -> int:
        # Keys outside of the range map to themselves
        if not self.is_in_range(key):
            return key

        # e.g. with (50, 14), 51 (51-50 = 1) will map to 14+1 = 15
        return self.target + (key - self.source)

    def is_in_range(self, key) -> bool:
        return self.source <= key < self.source_end

    @property
    def source_end(self):
        return self.source + self.size

    @property
    def target_end(self):
        return self.target + self.size

    @classmethod
    def from_string(cls, map_str: str):
        target, source, size = map_str.split()
        return cls(int(source), int(target), int(size))

    def __repr__(self):
        return f"{self.source} {self.target} {self.size}"


@dataclass
class RangeMapUnion:
    """Consider all ranges for mapping, falling back on the identity if none works.

    Not a very useful class in retrospect - didn't use it for part 2.
    """

    range_maps: list = field(default_factory=list)

    def __getitem__(self, key: int) -> int:
        for range_map in self.range_maps:
            if range_map.is_in_range(key):
                return range_map[key]

        return key


def parse_puzzle_input(puzzle_input: list[str]) -> tuple[list, dict]:
    almanach_maps = {}
    seeds = []

    section = None
    for line in puzzle_input:
        # Handle the special section separator case.
        if line == "":
            section = None
        # Handle the special seed case.
        elif line.startswith("seeds:"):
            seeds = [int(num) for num in line.split(":")[-1].split()]
        elif ":" in line:
            section = line.removesuffix(" map:")
            almanach_maps[section] = RangeMapUnion()
        else:
            range_map = RangeMap.from_string(line.split(":")[-1])
            almanach_maps[section].range_maps.append(range_map)

    return seeds, almanach_maps


def seed_to_location(seed: int, almanach_maps: dict) -> int:
    # Rely on the maps being already ordered in the input
    mapped_value = seed
    for map_type, range_map in almanach_maps.items():
        mapped_value = range_map[mapped_value]

    return mapped_value

## Part 
puzzle_input = utils.read_puzzle_input(sys.argv[1])
seeds, almanach_maps = parse_puzzle_input(puzzle_input)

# Part 1 ---------------------
print(min(seed_to_location(seed, almanach_maps) for seed in seeds))

# Part 2 ---------------------
def map_range(input_range: tuple[int, int], range_map: RangeMap) -> tuple[list, list]:
    """Map interval [a,b) with the map whose domain is [c,d).

    Returns a list of identity-mapped ranges and a list with the mapped range.
    """
    start, end = input_range

    #  --
    # ----
    if range_map.source <= start < end <= range_map.source_end:
        ret = ([], [(range_map[start], range_map[end - 1] + 1)])
    # ---              ---
    #     ---  or  ---
    elif (end <= range_map.source) or (range_map.source_end <= start):
        ret = ([(start, end)], [])
    # ----
    #  --
    elif start <= range_map.source < range_map.source_end <= end:
        initial = [(start, range_map.source)] if start < range_map.source else []
        tail = [(range_map.source_end, end)] if range_map.source_end < end else []
        ret = ([*initial, *tail], [(range_map.target, range_map.target_end)])
    # ----
    #   ----
    elif start < range_map.source < end < range_map.source_end:
        ret = (
            [(start, range_map.source)],
            [(range_map[range_map.source], range_map[end - 1] + 1)],
        )
    #   ----
    # ----
    elif range_map.source < start < range_map.source_end < end:
        ret = [(range_map.source_end, end)], [
            (range_map[start], range_map[range_map.source_end - 1] + 1)
        ]
    else:
        assert False

    assert all(a < b for a, b in ret[0] + ret[1]), ret
    return ret



seed_ranges = sorted([(a, a + b) for a, b in zip(seeds[::2], seeds[1::2])])

for map_name, maps in almanach_maps.items():
    next_maps_seeds = []

    for m in maps.range_maps:
        remaining_seeds = []
        for seed_range in seed_ranges:
            identity_ranges, mapped_ranges = map_range(seed_range, m)

            # The unmapped regions can be tried in the next maps.
            remaining_seeds.extend(identity_ranges)

            # The mapped regions go in the next round.
            next_maps_seeds.extend(mapped_ranges)

        seed_ranges = remaining_seeds

    seed_ranges = sorted(next_maps_seeds + remaining_seeds)

print(seed_ranges[0][0])
