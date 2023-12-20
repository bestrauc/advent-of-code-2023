import math
import sys
from collections import Counter, defaultdict, deque
from dataclasses import dataclass

import utils

puzzle = utils.read_puzzle_input(sys.argv[1])


@dataclass
class FlipFlop:
    state: bool = False

    def emit_pulse(self, src: str, pulse: bool) -> bool | None:
        if pulse:
            return

        self.state = not self.state
        return self.state


@dataclass
class Conjunction:
    state: dict[str, bool]

    def emit_pulse(self, src: str, pulse: bool) -> bool:
        self.state[src] = pulse
        return not all(self.state.values())


@dataclass
class Broadcast:
    def emit_pulse(self, src: str, pulse: bool) -> bool:
        return pulse


@dataclass
class Untyped:
    def emit_pulse(self, src: str, pulse: bool) -> None:
        return None


def main():
    modules = {}
    mod_types = {}
    for line in puzzle:
        module, targets = line.split(" -> ")
        targets = targets.split(", ")

        if module.startswith(("%", "&")):
            mod_type, mod_name = module[0], module[1:]
        elif module == "broadcaster":
            mod_type, mod_name = "b", module
        else:
            raise AssertionError(f"Failed to parse {line}")

        mod_types[mod_name] = mod_type
        modules[mod_name] = targets

    mod_states = {}
    for mod_name, mod_type in mod_types.items():
        if mod_type == "b":
            mod_states[mod_name] = Broadcast()
        elif mod_type == "%":
            mod_states[mod_name] = FlipFlop()
        else:
            inputs = [mod for mod, targets in modules.items() if mod_name in targets]
            mod_states[mod_name] = Conjunction({m: False for m in inputs})

    acc = Counter()
    for i in range(1000):
        c, _ = push_button(modules, mod_states, search="")
        acc += c

    # Part 1
    print(acc, acc[True] * acc[False])

    # Shamefully, I had a hint for this, which was to look at the graph.
    # We see that all the inputs to the final conjunction are FlipFlops.
    # Finding the iteration for which each of them sends a signal is easier
    # because of the much smaller search space. I assumed without proof that
    # each would fire in a certain cycle, which is confirmed by looking at
    # their firing patterns. The LCM of the cycles is then when they all fire.
    cycles = []
    for flip_node in ["xp", "xl", "gp", "ln"]:
        last = 0
        cycle = None
        for i in range(20000):
            _, found = push_button(modules, mod_states, search=flip_node)
            if found:
                cycle = i - last
                last = i
                print(flip_node, i, cycle)
        cycles.append(cycle)

    # Part 2
    print(math.lcm(*cycles))


def push_button(modules: dict, mod_states: dict, search: str) -> tuple[Counter, bool]:
    pulses = deque([(("button", "broadcaster"), False)])

    pulse_count = Counter()
    found = False
    while len(pulses) > 0:
        (src, target), pulse = pulses.popleft()
        pulse_count[pulse] += 1

        # Visualize the test input.
        # d = {False: "low", True: "high"}
        # print(f"{src} -{d[pulse]}-> {target}")

        if src == search and pulse:
            found = True

        next_pulse = mod_states.get(target, Untyped()).emit_pulse(src, pulse)
        if next_pulse is None:
            continue

        for next_target in modules[target]:
            pulses.append(((target, next_target), next_pulse))

    return pulse_count, found


main()
