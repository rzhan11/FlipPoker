import random
import numpy as np
import time


# Game settings
MAX_NUM_PLAYER_CARDS = 5
MIN_NUM_DEALER_CARDS = 8
DEALER_TAKES_TIES = True

# Game constants
NUM_RANKS = 13
NUM_SUITS = 4
NUM_CARDS = NUM_RANKS * NUM_SUITS



''' POKER HAND SCORES '''
STRAIGHT_FLUSH_PRIORITY =  8
FOUR_OF_A_KIND_PRIORITY =  7
FULL_HOUSE_PRIORITY =      6
FLUSH_PRIORITY =           5
STRAIGHT_PRIORITY =        4
THREE_OF_A_KIND_PRIORITY = 3
TWO_PAIR_PRIORITY =        2
PAIR_PRIORITY =            1
HIGH_CARD_PRIORITY =       0
INVALID_PRIORITY =        -1

priority_to_hand_name = {
    STRAIGHT_FLUSH_PRIORITY: "Straight flush",
    FOUR_OF_A_KIND_PRIORITY: "Four of a kind",
    FULL_HOUSE_PRIORITY: "Full house",
    FLUSH_PRIORITY: "Flush",
    STRAIGHT_PRIORITY: "Straight",
    THREE_OF_A_KIND_PRIORITY: "Three of a kind",
    TWO_PAIR_PRIORITY: "Two pair",
    PAIR_PRIORITY: "Pair",
    HIGH_CARD_PRIORITY: "High card",
    INVALID_PRIORITY: "Invalid",
}

STRAIGHT_LEN = 5
FLUSH_LEN = 5

''' Useful '''
index_to_card = [(i, j) for i in range(NUM_RANKS) for j in range(NUM_SUITS)]
card_to_index = {c: i for i, c in enumerate(index_to_card)}

MAX_RANDOM_VALS = 1000000
random_vals = np.random.uniform(size=MAX_RANDOM_VALS)
random_index = 0
'''        '''
