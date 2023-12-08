import itertools
import math
import sys

import utils

puzzle_input = utils.read_puzzle_input(sys.argv[1])
directions = puzzle_input[0]

def split_node_str(node_str: str) -> tuple[str, tuple[str, str]]:
    """Split AAA = (BBB,CCC) into (AAA, (BBB, CCC))"""
    source, target_str = node_str.split(" = ")
    targets = tuple([t.strip() for t in target_str.strip("()").split(",")])
    return source, targets

graph = dict([split_node_str(l) for l in puzzle_input[2:]])

# Part 1
current_node = "AAA"
for i, direction in enumerate(itertools.cycle(directions)):
    dir_idx = 0 if direction == "L" else 1
    next_node = graph[current_node][dir_idx]
    #print(f"{i}\t{current_node}->{next_node}")

    current_node = next_node
    if current_node == "ZZZ":
        break

print(f"Needed {i+1} steps to reach ZZZ from AAA.")
print()

# Part 2
# 
# It seems like after the nodes reach an end node, they enter a cycle
# from there on. They reach the end at i and then cycle every i steps.
# This must be some pecularity of the input, because I think they could
# also cycle like m + i*k, where they enter the cycle only after m steps.
#
# We measure the cycle lens c_i for each node and then want an l s.t.:
#
#   l = k_i * c_i
#
# for some k_i for each start node. This is the definition
# of the least common multiple of all the ci_s!

start_nodes = {n for n in graph.keys() if n.endswith("A")}
end_nodes = {n for n in graph.keys() if n.endswith("Z")}

print(f"Graph has {len(start_nodes)} start and {len(end_nodes)} end nodes.")

# By printing some cycles, I checked that it just so happens in this input
# that all are of the form i*k, so we stop at the first end node for each.
# Otherwise we'd have to employ some kind of cycle detection algorithm.
cycle_lens = []
for current_node in start_nodes:
    for i, direction in enumerate(itertools.cycle(directions)):
        dir_idx = 0 if direction == "L" else 1
        current_node = graph[current_node][dir_idx]

        if current_node in end_nodes:
            cycle_lens.append(i+1)
            break

all_in_end_node = math.lcm(*cycle_lens)
print(f"Needed {all_in_end_node} steps for all ghosts to arrive!")
