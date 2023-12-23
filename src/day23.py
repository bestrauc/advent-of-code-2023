"""
Part 1 was easy, but for part 2 I only managed the brute-force solution.
After checking out how other people did it, I learned of the graph compression
idea, which I then also implemented, though this is of course easy once you know
what to do.

So I can only count part 2 as half solved, with an ugly brute force approach.
"""
import sys
from collections import defaultdict

import utils

sys.setrecursionlimit(15000)

puzzle = [list(l) for l in utils.read_puzzle_input(sys.argv[1])]
h, w = utils.input_dim(puzzle)

start = (0, puzzle[0].index("."))
end = (h - 1, puzzle[h - 1].index("."))

# We can't go back to already visited nodes and also have
# these slopes, so it's a directed acyclic graph.
adj4 = {(-1, 0), (1, 0), (0, -1), (0, 1)}
slope_dir = {">": {(0, 1)}, "<": {(0, -1)}, "^": {(-1, 0)}, "v": {(1, 0)}}

# Create the adjacency graph.
graph = defaultdict(set)
weights = defaultdict(int)
for i in range(h):
    for j in range(w):
        if puzzle[i][j] == "#":
            continue

        for di, dj in adj4:
            ni, nj = (i + di, j + dj)
            if ni in range(h) and nj in range(w) and puzzle[ni][nj] != "#":
                graph[i, j].add((ni, nj))
                weights[(i, j), (ni, nj)] = 1

# Make dict to not get confused by defaultdict properties.
graph = dict(graph)

# Remove intermediate nodes that only connect two other nodes.
while any(len(adj) == 2 for adj in graph.values()):
    for node, adj in graph.items():
        if len(adj) == 2:
            break

    n1, n2 = adj
    graph[n1].add(n2)
    graph[n1].remove(node)

    graph[n2].add(n1)
    graph[n2].remove(node)

    weights[n1, n2] = weights[node, n1] + weights[node, n2]
    weights[n2, n1] = weights[node, n1] + weights[node, n2]

    del weights[node, n1]
    del weights[n1, node]
    del weights[n2, node]
    del weights[node, n2]
    del graph[node]

# Do a DFS to iterate over all paths from start to end, tracking the max.
dist_to_target = 0


def find_longest(node: tuple, visited_path: set, current_dist: int):
    global dist_to_target
    if node == end:
        dist_to_target = max(dist_to_target, current_dist)
        return

    visited_path.add(node)
    for neighbor in graph[node]:
        if neighbor in visited_path:
            continue

        edge_dist = weights[node, neighbor]
        find_longest(neighbor, visited_path, current_dist + edge_dist),

    visited_path.remove(node)


find_longest(start, set(), 0)
print(dist_to_target)
