import math
import re
import sys
from dataclasses import dataclass

from collections import Counter

@dataclass
class DrawingGame:
    id: int
    draws: list[Counter]

    @classmethod
    def from_input_line(cls, line: str):
        game, draw_str = line.split(":")
        game_id = int(game.split()[1])

        parsed_draws = []
        for draw_str in draw_str.split(";"):
            matches = re.findall(r"(\d+) (blue|red|green)", draw_str)
            parsed_draws.append(Counter({col: int(count) for count, col in matches}))

        return cls(id=game_id, draws=parsed_draws)

    def is_valid_game(self, bag_contents: Counter) -> bool:
        for draw in self.draws:
            # Wanted to try Counter diff, but requiring the copy is not so nice.
            # (bag_contents - draw) doesn't work, because it's more of a set diff.
            bag_diff = Counter(bag_contents)
            bag_diff.subtract(draw)
            if min(bag_diff.values()) < 0:
                return False

        return True

    def min_cubes_necessary(self) -> dict:
        result = Counter()

        for draw in self.draws:
            result |= draw

        return result


bag_contents = Counter({
    "red": 12,
    "green": 13,
    "blue": 14,
    })

lines = [line.strip() for line in open(sys.argv[1]).readlines()]
games = [DrawingGame.from_input_line(line) for line in lines]
valid_game_ids = [
    game.id for game in games if game.is_valid_game(bag_contents)
]

print(sum(valid_game_ids))

min_cube_powers = [
    math.prod(game.min_cubes_necessary().values()) for game in games
]
print(sum(min_cube_powers))
