import itertools
import sys
from dataclasses import dataclass, field

from tqdm import tqdm

import utils


@dataclass
class RangeMap:
    """Map a range as described in the task."""

    source: int
    target: int
    size: int

    def __getitem__(self, key: int) -> int:
        # Keys outside of the range map to themselves
        if not self.is_in_range(key):
            return key

        # e.g. with (50, 14), 51 (51-50 = 1) will map to 14+1 = 15
        return self.target + (key-self.source)

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
    """Consider all ranges for mapping, falling back on the identity if none works."""
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

puzzle_input = utils.read_puzzle_input(sys.argv[1])
seeds, almanach_maps = parse_puzzle_input(puzzle_input)

print(min(seed_to_location(seed, almanach_maps) for seed in seeds))
sys.exit()

# This doesn't work for part 2 of course.
seed_ranges = list(zip(seeds[::2], seeds[1::2]))
def is_in_seeds(val: int) -> bool:
    for seed_start, seed_length in seed_ranges:
        if seed_start <= val < seed_start+seed_length:
            return True
    
    return False
