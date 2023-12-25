import sys
import utils
from collections import defaultdict
from pprint import pprint

from heapq import *

from tqdm import tqdm

def min_cut(graph: dict, weights: dict) -> tuple[set, set, int]:
    """Stoer & Wagner minimum cut algorithm."""

    # Arbitrary start node
    s = list(graph.keys())[:1]

    # Store distances to set S in a heap.
    dists_to_s = [(-weights[s[0],v], v) for v in graph[s[0]]]
    breakpoint()

    # Iteratively add the strongest connected.
    for _ in tqdm(range(len(graph)-1)):
        strongest_connected = None
        strongest_dist = 0
        for v1 in graph.keys() - s:
            dist_to_s = sum([weights.get((v1, v2), 0) for v2 in s])
            if strongest_dist < dist_to_s:
                strongest_connected = v1
                strongest_dist = dist_to_s

        s.append(strongest_connected)

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

#while len(graph) > 1:
#    print(min_cut(graph, weights))

#pprint(graph)
#pprint(weights) 


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

    min_cut_weight = sys.maxsize
    min_cut_set = None
    while len(graph) > 1:
        print(len(graph))
        cut1, cut2, cut_weight = min_cut(graph, weights)

        if cut_weight < min_cut_weight:
            min_cut_set = set(cut1)
            min_cut_weight = cut_weight

    print(min_cut_set, min_cut_weight)

main()
