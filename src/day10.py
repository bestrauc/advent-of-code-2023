import sys
from collections import defaultdict

from shapely.geometry import Point, Polygon

import utils

sys.setrecursionlimit(50000)  # yolo


puzzle_input = utils.read_puzzle_input(sys.argv[1])


def input_to_graph(puzzle_input: list[str]):
    # Find start separately to let its neighbors link back from it.
    start = [
        (i, j)
        for i, line in enumerate(puzzle_input)
        for j, c in enumerate(line)
        if c == "S"
    ][0]

    adj_list = defaultdict(set)
    for i, line in enumerate(puzzle_input):
        for j, c in enumerate(line):
            neighbors = set()
            if c == "-":
                neighbors = {(i, j - 1), (i, j + 1)}
            elif c == "|":
                neighbors = {(i - 1, j), (i + 1, j)}
            elif c == "L":
                neighbors = {(i - 1, j), (i, j + 1)}
            elif c == "J":
                neighbors = {(i - 1, j), (i, j - 1)}
            elif c == "7":
                neighbors = {(i + 1, j), (i, j - 1)}
            elif c == "F":
                neighbors = {(i + 1, j), (i, j + 1)}
            elif c in {".", "S"}:
                pass
            else:
                raise AssertionError(f"Forgot {c}")

            # Prune -1 edge cases.
            neighbors = {
                (i, j)
                for (i, j) in neighbors
                if (0 <= i < len(puzzle_input)) and (0 <= j < len(line))
            }

            adj_list[(i, j)] |= neighbors

            # Populate the start's neighbors.
            for n in neighbors:
                if n == start:
                    adj_list[n].add((i, j))

    return start, adj_list


# Hacky, could be a property of the nodes, but oh well..
visited = set()


def find_path(
    current: tuple[int, int],
    prev: tuple[int, int],
    target: tuple[int, int],
    graph: dict[set],
) -> list[tuple[int, int]]:
    """DFS through the graph."""
    global visited

    visited.add(current)
    for neighbor in graph[current]:
        if (neighbor == target) and (neighbor != prev):
            return [current]

        if neighbor in visited:
            continue

        path = find_path(
            current=neighbor,
            prev=current,
            target=target,
            graph=graph,
        )
        if path is None:
            continue

        return [current] + path

    return None


if __name__ == "__main__":
    start, graph = input_to_graph(puzzle_input)
    path = find_path(current=start, prev=None, target=start, graph=graph)

    print(len(path) // 2)

    # Use a polygon intersection library. Pretty slow..
    contained = 0
    path_poly = Polygon(path + [path[0]])
    for i, line in enumerate(puzzle_input):
        for j, c in enumerate(line):
            contained += path_poly.contains(Point(i, j))

    print(contained)
