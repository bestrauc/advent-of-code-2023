import utils
import sys
import re
from collections import Counter

puzzle_inputs = utils.read_puzzle_input(sys.argv[1])

# NUM_COUNT = 5 # For the test cases.
NUM_COUNT = 10

def parse_card(card_line: str):
    num_matches = re.findall(r"(\d+)", card_line)
    card_num = int(num_matches[0])
    winning_nums = [int(n) for n in num_matches[1:NUM_COUNT+1]]
    drawn_nums = [int(n) for n in num_matches[NUM_COUNT+1:]]
    
    assert len(winning_nums) == len(set(winning_nums))
    assert len(drawn_nums) == len(set(drawn_nums))

    return card_num-1, (set(winning_nums), set(drawn_nums))

parsed_cards = dict([parse_card(card) for card in puzzle_inputs])

card_win_counts = [
    len(winners & drawn)
    for (winners, drawn) in parsed_cards.values()
]

# Part 1
print(sum(2**(win_count-1) for win_count in card_win_counts if win_count > 0))

# Zero-index the card counter for the loop.
card_counts = Counter(parsed_cards.keys())

# Part 2 - kind of slow at around 5s!
for card_id in range(len(card_counts.keys())):
    for repeat in range(card_counts[card_id]):
        card_wins = card_win_counts[card_id]

        max_won_card = min(len(card_counts.keys()), card_id+card_wins+1)
        for won_card in range(card_id+1, max_won_card):
            card_counts[won_card] += 1

print(sum(card_counts.values()))
