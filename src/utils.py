def read_puzzle_input(input_path: str) -> list[str]:
    return [l.strip() for l in open(input_path).readlines()]
