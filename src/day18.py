import sys
from dataclasses import dataclass

import numpy as np

import utils


@dataclass
class Dig:
    direction: str
    steps: int
    color: str

    @classmethod
    def from_str(cls, s: str) -> "Dig":
        direction, steps, color = s.split()
        return cls(direction=direction, steps=int(steps), color=color.strip("()"))

    @classmethod
    def from_str_part2(cls, s: str) -> "Dig":
        color = s.split()[-1]
        steps = int(color[2:7], 16)
        direction = {"0": "R", "1": "D", "2": "L", "3": "U"}[color[7]]

        return cls(direction=direction, steps=steps, color=color.strip("()"))


digs = [Dig.from_str(l) for l in utils.read_puzzle_input(sys.argv[1])]
digs2 = [Dig.from_str_part2(l) for l in utils.read_puzzle_input(sys.argv[1])]


def move_pos(dig: Dig, pos: tuple[int, int]) -> tuple[int, int]:
    match dig:
        case Dig("R", steps, _):
            return (pos[0], pos[1] + steps)
        case Dig("L", steps, _):
            return (pos[0], pos[1] - steps)
        case Dig("D", steps, _):
            return (pos[0] + steps, pos[1])
        case Dig("U", steps, _):
            return (pos[0] - steps, pos[1])
        case _:
            raise AssertionError(f"Forgot {dig}")


def compute_lagoon_volume(digs: list[Dig]) -> int:
    dig_path = [(0, 0)]
    for dig in digs:
        dig_path.append(move_pos(dig, pos=dig_path[-1]))

    dig_path = np.array(dig_path)

    # Length of the path boundary.
    path_len = np.abs(dig_path[1:, :] - dig_path[:-1, :]).max(axis=1).sum()

    # Shoelace formula (Trapezoid) for the polygon area.
    path_y = dig_path[:, 0]
    path_x = dig_path[:, 1]

    poly_area = np.abs(sum((path_y[1:] + path_y[:-1]) * (path_x[1:] - path_x[:-1])) / 2)

    # Now Pick's theorem, since we know the boundary points and area.
    interior_points = poly_area - path_len / 2 + 1

    return path_len + interior_points


print(compute_lagoon_volume(digs))
print(compute_lagoon_volume(digs2))
