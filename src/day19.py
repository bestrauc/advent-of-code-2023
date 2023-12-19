import math
import sys

import utils


def parse_workflow(s: str):
    label, rules = s[:-1].split("{")
    rule_strs = rules.split(",")

    target_rules = []
    for rule_str in rule_strs:
        rule_fields = rule_str.split(":")

        match rule_fields:
            case [target_label]:
                target_rules.append((target_label, "x", lambda x: True))
            case [rule_str, target_label]:
                var, condition = rule_str[0], rule_str[1:]
                rule = eval(f"lambda x: x{condition}")
                target_rules.append((target_label, var, rule))
            case _:
                raise Exception()

    return (label, target_rules)


def part_is_accepted(part: dict, workflows: dict):
    flow = "in"
    flow_history = ["in"]
    while flow not in {"A", "R"}:
        for target_label, var, rule in workflows[flow]:
            if rule(part[var]):
                flow = target_label
                break

        flow_history.append(flow)

    print("->".join(flow_history))
    return flow == "A"


def get_all_acceptance_flows(flow: str, workflows: dict) -> list:
    """Get all flows that lead to an A state.

    Also saves which condition in which workflow let us jump.
    """
    if flow == "A":
        yield [(None, flow)]

    for i, (target_flow, _, _) in enumerate(workflows.get(flow, [])):
        for h in get_all_acceptance_flows(target_flow, workflows):
            if len(h) > 0:
                yield [(i, flow), *h]


def count_flow_options(flow_nodes: list[str], workflows: dict) -> int:
    # Misuse sets as ranges for "convenience".
    # (It didn't turn out to be convenient..)
    possible_inputs = {
        "x": set(range(1, 4000 + 1)),
        "m": set(range(1, 4000 + 1)),
        "a": set(range(1, 4000 + 1)),
        "s": set(range(1, 4000 + 1)),
    }

    for (fi, flow), (_, next_flow) in zip(flow_nodes, flow_nodes[1:]):
        for i, (label, var, rule) in enumerate(workflows[flow]):
            jump_here = label == next_flow and i == fi

            # If we don't take this jump, filter out range that did *not* pass.
            filter_rule = rule if jump_here else (lambda x: not rule(x))

            possible_inputs = {
                k: v.copy() if k != var else set(filter(filter_rule, v))
                for k, v in possible_inputs.items()
            }

            if jump_here:
                break

    return math.prod([len(v) for v in possible_inputs.values()])


puzzle = utils.read_puzzle_input(sys.argv[1])
workflow_strs, part_strs = utils.split_list_at(puzzle, "")

parts = [eval(s.replace("{", "dict(").replace("}", ")")) for s in part_strs]
workflows = dict([parse_workflow(s) for s in workflow_strs])

# Part 1
print(sum([sum(p.values()) for p in parts if part_is_accepted(p, workflows)]))

# Part 2
accept_flows = list(get_all_acceptance_flows("in", workflows))
print(sum(count_flow_options(flow, workflows) for flow in accept_flows))
