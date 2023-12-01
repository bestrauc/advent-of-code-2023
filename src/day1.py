import re

puzzle = [l.strip() for l in open("inputs/input1.txt").readlines()]
digit_map = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}

def get_calibration_value(line):
    # Regex needs to do the lookahead thing to find overlapping words like twone.
    nums = re.findall(r"(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))", line)
    nums = [digit_map.get(n, n) for n in nums]
    return int(nums[0] + nums[-1])

print(sum(get_calibration_value(l) for l in puzzle))
