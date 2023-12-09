import sys

import utils

puzzle_input = utils.read_puzzle_input(sys.argv[1])
puzzle_input = list(map(utils.nums, puzzle_input))


def add_value(nums: list[int], forward: bool = True) -> list[int]:
    assert len(nums) > 0

    if all(n == 0 for n in nums):
        return (nums + [0]) if forward else ([0] + nums)

    num_diff = [b - a for a, b in zip(nums, nums[1:])]

    if forward:
        return nums + [nums[-1] + add_value(num_diff, forward)[-1]]
    else:
        return [nums[0] - add_value(num_diff, forward)[0]] + nums


print(sum(add_value(puzzle, forward=True)[-1] for puzzle in puzzle_input))
print(sum(add_value(puzzle, forward=False)[0] for puzzle in puzzle_input))
