SUIT_SYMBOLS = ["A", "B", "C", "D"]

def card_to_str(card):
    rank, suit = card
    return str(rank) + SUIT_SYMBOLS[suit]

def hand_to_str(cards):
    return [card_to_str(c) for c in cards]
