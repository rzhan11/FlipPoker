from game_constants import *
import poker_hands
import game
from pretty import card_to_str, hand_to_str
import utils

import random

def try_monte_carlo(policy, count):
    wins = 0
    for i in range(count):
        res = game.play_game(policy)
        if res > 0:
            wins += 1
    return wins

def probs_to_policy(probs):
    return lambda x, y: probs


tops = utils.get_cards_of_suit(4) \
        + utils.get_cards_of_suit(8) \
        + utils.get_cards_of_suit(9) \
        + utils.get_cards_of_suit(10) \
        + utils.get_cards_of_suit(11) \
        + utils.get_cards_of_suit(12)
top_probs = [0 if index_to_card[i] in tops else 1 for i in range(NUM_CARDS)]
top_policy = lambda x, y: top_probs
print("try", try_monte_carlo(top_policy, 10000))

def random_walk_monte_carlo():
    WALK_LEN = 1000000
    GAMES_PER_STEP = 10000
    SAVE_INTERVAL = 100

    cur_probs = [random.randint(0, 1) for j in range(NUM_CARDS)]
    cur_wins = 0
    cur_games = 0
    num_changes = 0
    for i in range(WALK_LEN):
        print("Step:", i)


        cur_cards = [index_to_card[i] for i in range(NUM_CARDS) if cur_probs[i] == 1]
        cur_policy = probs_to_policy(cur_probs)
        cur_wins += try_monte_carlo(cur_policy, GAMES_PER_STEP)
        cur_games += GAMES_PER_STEP
        print("Cur cards:", cur_cards)
        print("Cur wins:", cur_wins / cur_games * 100)

        new_probs = cur_probs[:]
        index = random.randint(0, NUM_CARDS - 1)
        new_probs[index] = 1 - new_probs[index]

        new_policy = probs_to_policy(new_probs)
        new_wins = try_monte_carlo(new_policy, GAMES_PER_STEP)
        new_games = GAMES_PER_STEP
        # print("New wins", new_wins)

        if new_wins / new_games > cur_wins / cur_games:
            cur_probs, cur_wins, cur_games = new_probs, new_wins, new_games
            print("Changed!")

        if i % SAVE_INTERVAL == 0:
            print("Saving!")
            with open(f"../data/random_walk/step_{i}.txt", "w") as f:
                f.write(str(cur_cards)+"\n")
                f.write(str(cur_wins) + " " + str(cur_games))
                f.write(str(cur_wins / cur_games))
        print("---\n")

    return cur_probs

random_walk_monte_carlo()

def greedy_monte_carlo(player_hand, dealer_hand):
    TRIALS = 100
    rem_cards = {i for i in range(NUM_CARDS)}
    for i in range(NUM_CARDS):
        card = index_to_card[i]
    num_cards_rem = NUM_CARDS - len(player_hand) - len(dealer_hand)
