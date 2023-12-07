import functools
import sys
from collections import Counter

import utils

card_ranking = list(
    reversed(
        [
            "A",
            "K",
            "Q",
            "T",
            "9",
            "8",
            "7",
            "6",
            "5",
            "4",
            "3",
            "2",
            "J",
        ]
    )
)


def score_hand_type(hand: str) -> int:
    card_counts = Counter(hand)
    vals = sorted(card_counts.values(), reverse=True)

    # Don't need to fill in Js for the JJJJJ case.
    # Variations: JJJJJ, AJJJJ, AAJJJ, AAAJJ, AAAAJ, AAAAA
    if (
        vals == [5]
        or (vals == [4, 1] and card_counts["J"] in {1, 4})
        or (vals == [3, 2] and card_counts["J"] in {2, 3})
    ):
        return 10

    # Now I don't want to figure this out anymore and brute-forcing combinations is manageable.
    possible_hands = generate_j_replacements(hand)
    possible_vals = [sorted(Counter(h).values(), reverse=True) for h in possible_hands]

    if any(vals == [4, 1] for vals in possible_vals):
        return 9

    if any(vals == [3, 2] for vals in possible_vals):
        return 8

    if any(vals == [3, 1, 1] for vals in possible_vals):
        return 7

    if any(vals == [2, 2, 1] for vals in possible_vals):
        return 6

    if any(vals == [2, 1, 1, 1] for vals in possible_vals):
        return 5

    if any(vals == [1, 1, 1, 1, 1] for vals in possible_vals):
        return 4

    raise AssertionError(f"Forgot to handle {hand} ({vals})")


@functools.cache
def generate_j_replacements(hand: str) -> str:
    """Not recommmended for len(hand) > 4."""

    if "J" not in hand:
        return [hand]

    repls = []
    for i, c in enumerate(hand):
        if c == "J":
            for r in card_ranking[1:]:
                new_hand = hand[:i] + r + hand[i + 1 :]
                new_replacements = generate_j_replacements(new_hand)
                repls.extend(new_replacements)

    return repls


def compare_hands(hand1: str, hand2: str) -> int:
    """Return -1 if hand1 < hand2, 0 if hand1 == hand2, else -2"""

    hand_type_rank1 = score_hand_type(hand1)
    hand_type_rank2 = score_hand_type(hand2)

    # If these aren't equal, return -1, 0 or 1
    if hand_type_rank1 != hand_type_rank2:
        return hand_type_rank1 - hand_type_rank2

    # Otherwise fall back to the other comparison.
    hand1_ranks = tuple([card_ranking.index(c) for c in hand1])
    hand2_ranks = tuple([card_ranking.index(c) for c in hand2])

    # Tuples are lexicographically comparable as needed.
    if hand1_ranks < hand2_ranks:
        return -1
    elif hand2_ranks < hand1_ranks:
        return 1
    else:
        return 0

puzzle_input = utils.read_puzzle_input(sys.argv[1])
hands_and_bids = [l.split() for l in puzzle_input]

sorted_hands_and_bids = sorted(hands_and_bids, key=lambda x: functools.cmp_to_key(compare_hands)(x[0]))

print(sum((i + 1) * int(bid) for i, (_hand, bid) in enumerate(sorted_hands_and_bids)))
