import sys
from collections import defaultdict
from dataclasses import dataclass, field
from heapq import *
from pprint import pprint
from typing import Any

import utils


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


def min_cut(graph: dict, weights: dict) -> tuple[set, set, int]:
    """Stoer & Wagner minimum cut algorithm."""

    # Arbitrary start node
    s = list(graph.keys())[:1]

    # Store distances to set S in a heap.
    dists_to_s = {v: weights[s[0], v] for v in graph[s[0]]}
    dist_heap = [PrioritizedItem(-dists_to_s[v], v) for v in graph[s[0]]]
    heapify(dist_heap)

    # Iteratively add the strongest connected.
    while len(s) < len(graph):
        prio_item = heappop(dist_heap)
        strongest_connected = prio_item.item
        strongest_dist = -1 * prio_item.priority

        # Deal with a node being added multiple times to the heap. If we
        # already consumed it with a higher distance, ignore later ones.
        if strongest_connected in s:
            continue

        s.append(strongest_connected)

        # Now we have to add the neighbors of the strongest connected
        # to the heap or update their weights.
        for v in graph[strongest_connected]:
            dists_to_s.setdefault(v, 0)
            dists_to_s[v] += weights[strongest_connected, v]
            heappush(dist_heap, PrioritizedItem(-dists_to_s[v], v))

    # Merge the last two in s.
    merge_nodes(s[-1], s[-2], graph, weights)

    return s[:-1], s[-1], strongest_dist


def merge_nodes(v1, v2, graph: dict, weights: dict):
    vnew = (v1, v2)

    # Merge the two nodes
    graph[vnew] = graph[v1] | graph[v2]
    del graph[v1]
    del graph[v2]

    for v in list(graph.keys()):
        # Add a new edge to the merged node if necessary.
        # Also deal with adapting incoming and outgoing edge weights.
        if v1 in graph[v] or v2 in graph[v]:
            graph[v].add(vnew)

            # Note the side effect of pop - we delete the old edge weights as well.
            weights[(v, vnew)] = weights.pop((v, v1), 0) + weights.pop((v, v2), 0)
            weights[(vnew, v)] = weights.pop((v1, v), 0) + weights.pop((v2, v), 0)

        # Remove any incoming edges to the old nodes.
        graph[v] = graph[v] - {v1, v2}


def test_stoer_wagner():
    """Test my Stoer-Wagner algorithm implementation.

    I've implemented the minimum-cut algorithm based on these lecture slides:
    https://i11www.iti.kit.edu/_media/teaching/winter2012/algo2/vorlesung5.pdf

    I used the example graph to validate that my implementation seems correct.
    """
    test_graph = {
        1: [(2, 2), (5, 3)],
        2: [(1, 2), (5, 2), (6, 2), (3, 3)],
        3: [(2, 3), (7, 2), (4, 4)],
        4: [(3, 4), (7, 2), (8, 2)],
        5: [(1, 3), (2, 2), (6, 3)],
        6: [(5, 3), (2, 2), (7, 1)],
        7: [(6, 1), (3, 2), (4, 2), (8, 3)],
        8: [(7, 3), (4, 2)],
    }

    weights = {(v1, v2): w for (v1, ns) in test_graph.items() for (v2, w) in ns}
    graph = {v1: {v2 for (v2, _) in ns} for (v1, ns) in test_graph.items()}

    # pprint(graph)
    # pprint(weights)

    while len(graph) > 1:
        print(min_cut(graph, weights))


def main():
    puzzle = utils.read_puzzle_input(sys.argv[1])

    graph = defaultdict(set)
    weights = {}
    for line in puzzle:
        node, connected = line.split(": ")
        for conn in connected.split(" "):
            graph[node].add(conn)
            graph[conn].add(node)

            weights[(node, conn)] = 1
            weights[(conn, node)] = 1

    original_size = len(graph)
    min_cut_weight = sys.maxsize
    min_cut_set = None
    while len(graph) > 1:
        print(len(graph))
        cut1, cut2, cut_weight = min_cut(graph, weights)

        if cut_weight < min_cut_weight:
            min_cut_set = set(cut1)
            min_cut_weight = cut_weight

        # Save a bit of time.
        if cut_weight == 3:
            break

    cut_set_size = len(list(flatten(min_cut_set)))
    print(cut_set_size, original_size - cut_set_size, min_cut_weight)


def flatten(d):
    """My implementation ends up with many merged nodes -> unmerge to count them."""

    for i in d:
        yield from [i] if not isinstance(i, tuple) else flatten(i)


main()
