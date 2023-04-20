from game_constants import *

def get_cards_of_suit(suit):
    return [(r, suit) for r in range(NUM_RANKS)]

def get_cards_of_rank(rank):
    return [(rank, s) for s in range(NUM_SUITS)]
