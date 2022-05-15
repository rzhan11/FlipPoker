from game_constants import *
from pretty import card_to_str, hand_to_str


def get_best_poker_hand(hand):
    cards = set(index_to_card[ind] for ind in hand)

    # straight flush
    sf_score, sf_poker_hand = check_straight_flush(cards)
    if sf_poker_hand is not None:
        return sf_score, sf_poker_hand

    cards_by_suit, cards_by_rank = get_card_partitions(cards)

    # four of a kinds, full houses, three of a kinds, 2 pairs, pairs, high card
    ranked_score, ranked_poker_hand = check_ranked_hands(cards, cards_by_rank)
    suited_score, suited_poker_hand = check_suited_hands(cards_by_suit)
    straight_score, straight_poker_hand = check_straight(cards_by_rank)

    scores = [(ranked_score, ranked_poker_hand), (suited_score, suited_poker_hand), (straight_score, straight_poker_hand)]


    scores.sort(reverse=True)

    return scores[0]


def check_straight_flush(cards):
    straight_flushes = []
    # check for straight flush in each of the suits
    for suit in range(NUM_SUITS):
        straight_len = 0
        prev_cards = []
        rank_order = reversed([NUM_RANKS - 1] + [i for i in range(NUM_RANKS)])
        for rank in rank_order:
            if (rank, suit) in cards:
                straight_len += 1
                prev_cards += [(rank, suit)]
                if straight_len == STRAIGHT_LEN:
                    straight_flushes += [(rank, prev_cards)]
                    break
            else:
                straight_len, prev_cards = 0, []

    if len(straight_flushes) > 0:
        best_rank, best_cards = -1, []
        for rank, cards in straight_flushes:
            if rank > best_rank:
                best_rank, best_cards = rank, cards
        return (STRAIGHT_FLUSH_PRIORITY, [best_rank + STRAIGHT_LEN - 1]), best_cards
    else:
        return (INVALID_PRIORITY, []), None


def check_straight(cards_by_rank):
    prev_cards = []
    straight_len = 0
    rank_order = reversed([NUM_RANKS - 1] + [i for i in range(NUM_RANKS)])
    for rank in rank_order:
        if len(cards_by_rank[rank]) > 0:
            straight_len += 1
            prev_cards += [cards_by_rank[rank][0]]
            if straight_len == STRAIGHT_LEN:
                top_card = rank + STRAIGHT_LEN - 1
                return (STRAIGHT_PRIORITY, [top_card]), prev_cards
        else:
            straight_len, prev_cards = 0, []
    return (INVALID_PRIORITY, []), None


def add_kickers(my_cards, sorted_cards):
    kicker_ranks = []
    for c in sorted_cards:
        if c not in my_cards:
            kicker_ranks += [c[0]]
            my_cards += [c]
            if len(my_cards) == MAX_NUM_PLAYER_CARDS:
                break
    if len(my_cards) < MAX_NUM_PLAYER_CARDS:
        kicker_ranks += [-1] * (MAX_NUM_PLAYER_CARDS - len(my_cards))
    return my_cards, kicker_ranks


def get_card_partitions(cards):
    cards_by_rank = [[] for i in range(NUM_RANKS)]
    cards_by_suit = [[] for i in range(NUM_SUITS)]
    for c in cards:
        cards_by_rank[c[0]] += [c]
        cards_by_suit[c[1]] += [c]
    return cards_by_suit, cards_by_rank


# checks for pairs, triples, full houses, four of a kinds
def check_ranked_hands(all_cards, cards_by_rank):
    sorted_cards = sorted(all_cards, reverse=True, key=lambda x: x[0])
    # print(sorted_cards)

    rank4 = []
    rank3 = []
    rank2 = []
    rank1 = []

    # find four of a kind

    for rank in range(NUM_RANKS):
        cards = cards_by_rank[rank]
        if len(cards) == 1:
            rank1 += [(rank, cards)]
        elif len(cards) == 2:
            rank2 += [(rank, cards)]
        elif len(cards) == 3:
            rank3 += [(rank, cards)]
        elif len(cards) == 4:
            rank4 += [(rank, cards)]

    if len(rank4) >= 1:
        quad_rank, quad_cards = rank4[-1]
        return (FOUR_OF_A_KIND_PRIORITY, [quad_rank]), quad_cards

    if len(rank3) >= 1:
        triple_rank, triple_cards = rank3[-1]
        pair_kicker_rank = -1
        pair_kicker_cards = []
        if len(rank2) > 0:
            pair_kicker_rank, pair_kicker_cards = rank2[-1]
        if len(rank3) > 1 and rank3[-2][0] > pair_kicker_rank:
            pair_kicker_rank, pair_kicker_cards = rank3[-2]
        # full house
        if pair_kicker_rank >= 0:
            my_cards = triple_cards + pair_kicker_cards
            return (FULL_HOUSE_PRIORITY, [triple_rank, pair_kicker_rank]), triple_cards + pair_kicker_cards

        # three of a kind
        my_cards, kicker_ranks = add_kickers(triple_cards, sorted_cards)
        return (THREE_OF_A_KIND_PRIORITY, [triple_rank] + kicker_ranks), my_cards

    # two pairs
    if len(rank2) >= 2:
        pair1_rank, pair1_cards = rank2[-1]
        pair2_rank, pair2_cards = rank2[-2]
        my_cards, kicker_ranks = add_kickers(pair1_cards + pair2_cards, sorted_cards)
        return (TWO_PAIR_PRIORITY, [pair1_rank, pair2_rank] + kicker_ranks), my_cards

    # one pair
    if len(rank2) >= 1:
        pair_rank, pair_cards = rank2[-1]
        my_cards, kicker_ranks = add_kickers(pair_cards, sorted_cards)
        return (PAIR_PRIORITY, [pair_rank] + kicker_ranks), my_cards

    # high card
    my_cards, kicker_ranks = add_kickers([], sorted_cards)
    # print(my_cards, kicker_ranks)
    return (HIGH_CARD_PRIORITY, kicker_ranks), my_cards


def compare_flushes(flush1, flush2):
    for s1, s2 in zip(flush1, flush2):
        if s1 != s2:
            return s1 - s2
    return 0


def check_suited_hands(cards_by_suit):
    flushes = []
    for suit in range(NUM_SUITS):
        cards = cards_by_suit[suit]
        if len(cards) >= FLUSH_LEN:
            cards = sorted(cards, reverse=True, key=lambda x: x[0])[:5]
            ranks = [c[0] for c in cards]
            flushes += [(ranks, cards)]

    if len(flushes) > 0:
        best_flush_ranks = [-1 for i in range(FLUSH_LEN)]
        best_flush_cards = None
        for ranks, cards in flushes:
            if compare_flushes(ranks, best_flush_ranks) > 0:
                best_flush_ranks, best_flush_cards = ranks, cards
        return (FLUSH_PRIORITY, best_flush_ranks), best_flush_cards
    else:
        return (INVALID_PRIORITY, []), None


def compare_poker_score(score1, score2):
    p1, tiebreakers1 = score1
    p2, tiebreakers2 = score2
    if p1 != p2:
        return p1 - p2
    for k1, k2 in zip(tiebreakers1, tiebreakers2):
        if k1 != k2:
            return k1 - k2
    return 0
