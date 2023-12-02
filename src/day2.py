import math
import re
import sys
from dataclasses import dataclass


@dataclass
class DrawingGame:
    id: int
    draws: list[dict]

    @classmethod
    def from_input_line(cls, line: str):
        game, draw_str = line.split(":")
        game_id = int(game.split()[1])

        parsed_draws = []
        for draw_str in draw_str.split(";"):
            matches = re.findall(r"(\d+) (blue|red|green)", draw_str)
            parsed_draws.append({col: int(count) for count, col in matches})

        return cls(id=game_id, draws=parsed_draws)

    def is_valid_game(self, bag_contents: dict) -> bool:
        for draw in self.draws:
            for col, num in bag_contents.items():
                if draw.get(col, 0) > num:
                    return False

        return True

    def min_cubes_necessary(self) -> dict:
        result = {"green": 0, "red": 0, "blue": 0}

        for draw in self.draws:
            for color, count in draw.items():
                result[color] = max(result[color], count)

        return result


bag_contents = {
    "red": 12,
    "green": 13,
    "blue": 14,
    }


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
