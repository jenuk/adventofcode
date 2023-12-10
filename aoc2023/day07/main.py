from typing import Any
from typing_extensions import Self
from aoc_helper.utils import load_lines, timeit


def get_type_p1(hand: str) -> int:
    hand_set = set(hand)
    num_cards = len(hand_set)
    if num_cards == 5:
        # high card
        return 1
    elif num_cards == 4:
        # one pair
        return 2
    elif num_cards == 3:
        # two pair or three of a kind
        is_three = max(hand.count(ch) for ch in hand_set) == 3
        return 3 + is_three
    elif num_cards == 2:
        # full hourse or four of a kind
        is_four = max(hand.count(ch) for ch in hand_set) == 4
        return 5 + is_four
    elif num_cards == 1:
        return 7
    else:
        raise NotImplementedError("Hand too large")


def get_type_p2(hand: str) -> int:
    joker_count = hand.count("J")
    hand_new = [ch if ch != "J" else chr(ord("a") + k) for k, ch in enumerate(hand)]
    tier = get_type_p1("".join(hand_new))
    if joker_count == 0:
        return tier
    elif joker_count == 1:
        # full house and five not possible
        if tier == 1 or tier == 6:
            # high card, four of a kind
            return tier + 1
        else:
            # one pair, two pair, three of a kind can skip one tier
            return tier + 2
    elif joker_count == 2:
        # full hourse, five, four, two pair not possible
        if tier == 1 or tier == 4:
            # high card, three of a kind
            return tier + 3
        else:
            # one pair
            return tier + 4
    elif joker_count == 3:
        # possible: high card, one pair
        return tier + 5
    else:
        # four or five joker -> five of kind total
        return 7


class Hand:
    def __init__(self, hand: str, order_dict: dict[str, int], joker: bool = False):
        self.hand = hand
        self.rank = get_type_p2(hand) if joker else get_type_p1(hand)
        self.order_dict = order_dict

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Hand):
            return False
        return self.hand == other.hand

    def __lt__(self, other: Self) -> bool:
        if self.rank != other.rank:
            return self.rank < other.rank
        for ch1, ch2 in zip(self.hand, other.hand):
            if ch1 == ch2:
                continue
            return self.order_dict[ch1] < self.order_dict[ch2]
        # Equal hand
        return False

    def __le__(self, other: Self) -> bool:
        if self.rank != other.rank:
            return self.rank < other.rank
        for ch1, ch2 in zip(self.hand, other.hand):
            if ch1 == ch2:
                continue
            return self.order_dict[ch1] <= self.order_dict[ch2]
        # Equal hand
        return True


@timeit
def main(fn: str):
    order = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    order_dict = {c: k for k, c in enumerate(order[::-1])}

    lines = load_lines(fn)
    hands = []
    for line in lines:
        hand, bid = line.split(" ")
        hands.append((Hand(hand, order_dict, joker=False), int(bid)))

    total_p1 = 0
    hands.sort()
    for k, (_, bid) in enumerate(hands):
        total_p1 += (k + 1) * bid

    order = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
    order_dict = {c: k for k, c in enumerate(order[::-1])}
    hands_new = []
    for hand, bid in hands:
        hands_new.append((Hand(hand.hand, order_dict, joker=True), bid))
    total_p2 = 0
    hands_new.sort()
    for k, (_, bid) in enumerate(hands_new):
        total_p2 += (k + 1) * bid

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
