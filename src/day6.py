import utils
import sys


puzzle_input = utils.read_puzzle_input(sys.argv[1])

# Part 1
races = list(zip(utils.nums(puzzle_input[0]), utils.nums(puzzle_input[1])))
print(races)

# Part 2
times, dists = zip(*races)
races = [(
    int(''.join(map(str, times))),  # Concatenate times
    int(''.join(map(str, dists))))  # Concatenate distances
]
print(races)

# We assume there's a large stretch of winning configurations,
# so we'll find the start and end of that region to save time.
acc = 1
for (time, dist) in races:
    win_start = None
    for t in range(time+1):
        if t*(time-t) > dist:
            win_start = t
            break

    win_end = None
    for t in reversed(range(time+1)):
        if t*(time-t) > dist:
            win_end = t
            break

    acc *= (win_end-win_start+1)

print(acc)
