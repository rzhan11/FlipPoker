import random
import numpy as np
import time

from game_constants import *
from poker_hands import get_best_poker_hand, compare_poker_score
from pretty import card_to_str, hand_to_str



example_deck = [i for i in range(NUM_CARDS)]
def new_deck():
    deck = example_deck[:]
    random.shuffle(deck)
    return deck


# STATE = (player_hand, dealer_hand, deck, deck_index)
# player_wants_prob: size 52 array, representing probability that they want this card
def play_turn(player_wants, player_hand, dealer_hand, deck, deck_index):
    # draw until hits
    while deck_index < NUM_CARDS:
        card = deck[deck_index]
        deck_index += 1

        if player_wants[card]: # player gets card
            player_hand += [card]
            break
        else: # dealer gets card
            dealer_hand += [card]

    # if reach here, then game is over since deck is empty
    return player_hand, dealer_hand, deck_index



def get_winner(player_hand, dealer_hand):
    # check for royal flush
    player_score, player_poker_hand = get_best_poker_hand(player_hand)
    dealer_score, dealer_poker_hand = get_best_poker_hand(dealer_hand)

    # print("Player:")
    # print("\t", player_score)
    # print("\t", hand_to_str(player_poker_hand))
    #
    # print("Dealer")
    # print("\t", dealer_score)
    # print("\t", hand_to_str(dealer_poker_hand))

    return compare_poker_score(player_score, dealer_score)


# returns 1 if player wins, -1 if dealer wins
def play_game(get_wants, player_hand_start=[], dealer_hand_start=[]):
    player_hand, dealer_hand = player_hand_start[:], dealer_hand_start[:]
    deck, deck_index = new_deck(), (len(player_hand) + len(dealer_hand))
    while True:
        # get player wants
        player_wants = get_wants(player_hand, dealer_hand)
        # complete turn
        player_hand, dealer_hand, deck_index = play_turn(player_wants, player_hand, dealer_hand, deck, deck_index)
        # check if game is over
        if len(player_hand) == MAX_NUM_PLAYER_CARDS or deck_index == NUM_CARDS:
            break

    # do post-draw operations
    # if dealer needs more cards
    if len(dealer_hand) < MIN_NUM_DEALER_CARDS:
        rem_cards = MIN_NUM_DEALER_CARDS - len(dealer_hand)
        dealer_hand += deck[deck_index: deck_index + rem_cards]

    result = get_winner(player_hand, dealer_hand)

    if result > 0:
        return 1
    else:
        return -1
