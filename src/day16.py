import itertools
import sys
from collections import Counter
from dataclasses import dataclass, field
from typing import ClassVar

import numpy as np  # Want to add coords.
from tqdm import tqdm

import utils


@dataclass
class BeamNode:
    coord: np.array
    direction: np.array
    grid: np.array

    children: list["BeamNode"] = field(init=False, default_factory=lambda: [])

    # Ensure we don't keep making beam nodes for cycles.
    node_visited: ClassVar[set["BeamNode"]] = set()

    def move_beam(self) -> list["BeamNode"]:
        """Move the beam depending where it is, return the new location(s)."""

        beams = []
        match (self.grid[self.coord[0]][self.coord[1]], tuple(self.direction)):
            # Moving through empty space or through the pointy end of splitter.
            case (".", _) | ("-", (0, _)) | ("|", (_, 0)):
                beams = [BeamNode(self.coord + self.direction, self.direction, self.grid)]
            # Come at ->\ or /<-, so we go down.
            case ("\\", (0, 1)) | ("/", (0, -1)):
                new_direction = (1, 0)
                beams = [BeamNode(self.coord + new_direction, new_direction, self.grid)]
            # Come at \<- or ->/, so we go up.
            case ("\\", (0, -1)) | ("/", (0, 1)):
                new_direction = (-1, 0)
                beams = [BeamNode(self.coord + new_direction, new_direction, self.grid)]
            # Come at ↑\ or ↓/, so we go left.
            case ("\\", (-1, 0)) | ("/", (1, 0)):
                new_direction = (0, -1)
                beams = [BeamNode(self.coord + new_direction, new_direction, self.grid)]
            # Come at \↓ or /↑, so we go right.
            case ("\\", (1, 0)) | ("/", (-1, 0)):
                new_direction = (0, 1)
                beams = [BeamNode(self.coord + new_direction, new_direction, self.grid)]
            # Hit horizontal splitter from left or right -> go up and down.
            case ("|", _):
                new_direction1 = (1, 0)
                new_direction2 = (-1, 0)
                beams = [
                    BeamNode(self.coord + new_direction1, new_direction1, self.grid),
                    BeamNode(self.coord + new_direction2, new_direction2, self.grid),
                ]
            # Hit vertical splitter from top or bottom -> go left and right.
            case ("-", _):
                new_direction1 = (0, -1)
                new_direction2 = (0, 1)
                beams = [
                    BeamNode(self.coord + new_direction1, new_direction1, self.grid),
                    BeamNode(self.coord + new_direction2, new_direction2, self.grid),
                ]
            case _:
                print(self.grid[self.coord[0]][self.coord[1]], tuple(self.direction))
                raise AssertionError("Forgot something")

        # Filter out beams that are out of bounds or entered a cycle.
        beams = [b for b in beams if b.in_grid and not b.visited_before]

        self.children = beams
        BeamNode.node_visited.add(self)
        return beams

    @property
    def in_grid(self) -> bool:
        return (0 <= self.coord[0] < self.grid.shape[0]) and (
            0 <= self.coord[1] < self.grid.shape[1]
        )

    @property
    def visited_before(self) -> bool:
        return self in BeamNode.node_visited

    def __hash__(self) -> int:
        return hash((*self.coord, *self.direction))

    def __eq__(self, other: "BeamNode") -> bool:
        return hash(self) == hash(other)

    def __repr__(self) -> str:
        return f"{self.coord} ({self.direction}, in_grid={self.in_grid})"

    @classmethod
    def clear_visitation_cache(cls):
        cls.node_visited = set()


puzzle_input = np.array(list(map(list, utils.read_puzzle_input(sys.argv[1]))))
print(puzzle_input.shape)


def count_energized(beam: BeamNode, cells: set) -> int:
    cells |= {tuple(beam.coord)}

    for child in beam.children:
        cells |= count_energized(child, cells)

    return cells


def energized_from_start(coord: tuple[int, int], direction: tuple[int, int]) -> int:
    BeamNode.clear_visitation_cache()
    beam_root = BeamNode(
        coord=np.array(coord),
        direction=np.array(direction),
        grid=puzzle_input,
    )

    beams = [beam_root]
    while len(beams) > 0:
        beams = [moved for b in beams for moved in b.move_beam()]

    return len(count_energized(beam_root, cells=set()))


# Part 1
print(energized_from_start((0, 0), (0, 1)))

# Part 2
height, width = puzzle_input.shape
candidates = []
candidates += [((0, j), (1, 0)) for j in range(width)]
candidates += [((height - 1, j), (-1, 0)) for j in range(width)]
candidates += [((i, 0), (0, 1)) for i in range(height)]
candidates += [((i, width - 1), (0, -1)) for i in range(height)]

# We could employ a cache of energized cells along previously computed
# paths here, which would make this fairly instant, but after trying a
# bit, I didn't want to refactor things further and just brute-force.
print(
    max(energized_from_start(coord, direction) for coord, direction in tqdm(candidates))
)
