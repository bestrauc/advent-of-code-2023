import queue
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any

import numpy as np

import utils


# Probably useless and confusing in retrospect.
# I should have used a bunch of arrays to store distances, etc.
@dataclass(order=True)
class PrioritizedItem:
    dist: int
    item: Any = field(compare=False)
    prev: Any = field(compare=False, default=None)

    # Hack to invalidate queued items whose distance changed.
    ignore: bool = field(compare=False, default=False)

    def __repr__(self) -> str:
        return f"{self.item} ({self.dist})"


def shortest_path(start: tuple, goal: tuple, graph: dict):
    active = queue.PriorityQueue()
    node_dict = {}
    for n in graph.keys():
        item = PrioritizedItem(dist=0 if (n == start) else sys.maxsize, item=n)
        node_dict[n] = item
        active.put(item)

    while not active.empty():
        node = active.get()
        if node.ignore:
            continue

        # Found the smallest path to node at this point.
        if node.item[:2] == goal:
            return node

        for neigh_pos, neighbor_weight in graph[node.item]:
            neighbor = node_dict[neigh_pos]

            if node.dist + neighbor_weight <= neighbor.dist:
                # Awkward vertex invalidation and re-adding because
                # PriorityQueue has no priority changing API.
                neighbor.ignore = True
                updated_neighbor = PrioritizedItem(
                    dist=node.dist + neighbor_weight,
                    item=neighbor.item,
                    prev=node,
                )
                node_dict[neigh_pos] = updated_neighbor
                active.put(updated_neighbor)

    return None


puzzle = np.array([[int(heat) for heat in line] for line in utils.read_puzzle_input(sys.argv[1])])

MIN_MV = 4
MAX_MV = 10

graph = {}  # Adjacency list with weights.
for i in range(puzzle.shape[0]):
    mi = puzzle.shape[0] - i - 1  # mirrored index
    for j in range(puzzle.shape[1]):
        mj = puzzle.shape[1] - j - 1  # mirrored index

        # Very cumbersome graph construction. We need to search not only a space of
        # 2D coordinates, but also track from which direction a position was reached
        # (horizontally or vertically) to not miss out on exploring good paths.
        #
        # For example, below, the naive solution is >>vvv>>v (cost 10), even if you
        # already constructed the graph to account for at most 3 steps per direction.
        # The correct solution is v>>vvv>>, but the v>> has a higher cost than >>v,
        # so you can't stop at (1,2) naively.
        #
        #       11199
        #       12199
        #       99199
        #       99131
        #       99111
        #
        # So we force the algorithm to keep both options open by extending the graph
        # to a (i,j,direction) dimension, which prevents states from being removed
        # from the priority queue too early.
        neighbors = [
            ((i, j + dj + MIN_MV, "h"), heat)
            for dj, heat in enumerate(np.cumsum(puzzle[i, j + 1 :])[MIN_MV - 1 : MAX_MV])
        ]
        neighbors += [
            ((i, j - (dj + MIN_MV), "h"), heat)
            for dj, heat in enumerate(np.cumsum(np.fliplr(puzzle)[i, mj + 1 :])[MIN_MV - 1 : MAX_MV])
        ]
        # A node that was reached vertically has horizontal neighbors.
        graph[(i, j, "v")] = neighbors

        neighbors = [
            ((i + di + MIN_MV, j, "v"), heat)
            for di, heat in enumerate(np.cumsum(puzzle[i + 1 :, j])[MIN_MV - 1 : MAX_MV])
        ]
        neighbors += [
            ((i - (di + MIN_MV), j, "v"), heat)
            for di, heat in enumerate(np.cumsum(np.flipud(puzzle)[mi + 1 :, j])[MIN_MV - 1 : MAX_MV])
        ]
        # A node that was reached horizontally has vertical neighbors.
        graph[(i, j, "h")] = neighbors

graph[(0, 0)] = graph[(0, 0, "v")] + graph[(0, 0, "h")]


tmp = shortest_path(
    start=(0, 0),
    goal=(puzzle.shape[0] - 1, puzzle.shape[1] - 1),
    graph=graph,
)

print(tmp.dist)
sys.exit()

# Debugging print code.

sign = lambda x: x and (1, -1)[x < 0]

grid = puzzle.astype(str)
while tmp.prev is not None:
    move = (tmp.item[0] - tmp.prev.item[0], tmp.item[1] - tmp.prev.item[1])
    normalized = (sign(move[0]), sign(move[1]))
    match normalized:
        case (0, -1):
            char = "<"
        case (0, 1):
            char = ">"
        case (1, 0):
            char = "v"
        case (-1, 0):
            char = "^"

    for i in range(max(abs(move[0]), abs(move[1]))):
        grid[(tmp.item[0] - normalized[0] * i, tmp.item[1] - normalized[1] * i)] = char

    tmp = tmp.prev

print("\n".join(["".join(map(str, l)) for l in grid]))
