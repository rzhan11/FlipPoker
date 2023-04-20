# game constants
NUM_RANKS = 13
NUM_SUITS = 4
NUM_CARDS = NUM_RANKS * NUM_SUITS
CARDS = [(s, r) for s in range(NUM_SUITS) for r in range(NUM_RANKS)]

STRAIGHT_FLUSH_LEN = 5
STRAIGHT_LEN = 5
FLUSH_LEN = 5
FOUR_KIND_LEN = 4
THREE_KIND_LEN = 3
TWO_KIND_LEN = 2


# ratings
RATING_TYPE_OFFSET = 2 * NUM_RANKS

STRAIGHT_FLUSH_RATING = 9 << RATING_TYPE_OFFSET
FOUR_KIND_RATING = 8 << RATING_TYPE_OFFSET
FULL_HOUSE_RATING = 7 << RATING_TYPE_OFFSET
FLUSH_RATING = 6 << RATING_TYPE_OFFSET
STRAIGHT_RATING = 5 << RATING_TYPE_OFFSET
THREE_KIND_RATING = 4 << RATING_TYPE_OFFSET
TWO_PAIR_RATING = 3 << RATING_TYPE_OFFSET
TWO_KIND_RATING = 2 << RATING_TYPE_OFFSET
ONE_KIND_RATING = 1 << RATING_TYPE_OFFSET


RATING_TYPE_MASK = 15 << RATING_TYPE_OFFSET
RATING_KICKER2_MASK = (1 << NUM_RANKS) - 1
RATING_KICKER1_MASK = RATING_KICKER2_MASK << NUM_RANKS


"""
- _suit_mask: _suit_mask[s] gives bit mask for all cards of suit s
- _bit_mask: _bit_mask[ind] gives bit mask for bitind 'ind'
- _bit_mask2: _bit_mask2[s][r] gives bit mask for card (s, r)
"""

ALL_BITS = (1 << NUM_CARDS) - 1
BIT = [1 << i for i in range(NUM_CARDS)]
BIT2 = [[(1 << (s * NUM_RANKS + r)) for r in range(NUM_RANKS)] for s in range(NUM_SUITS)]

UNBIT = {m: i for i, m in enumerate(BIT)}
UNBIT[0] = -1

SUIT_MASKS = [((1 << NUM_RANKS) - 1) << (s * NUM_RANKS) for s in range(NUM_SUITS)]
RANK_MASKS = [sum([1 << (s * NUM_RANKS + r) for s in range(NUM_SUITS)]) for r in range(NUM_RANKS)]

SUIT_MASK = SUIT_MASKS[0]