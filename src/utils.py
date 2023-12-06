import re

def read_puzzle_input(input_path: str) -> list[str]:
    return [l.strip() for l in open(input_path).readlines()]

def nums(line: str) -> list[int]:
    return [int(n) for n in re.findall(r"(\d+)", line)]
