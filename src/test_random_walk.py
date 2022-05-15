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


# tops = [(4, 0), (4, 1), (4, 2), (4, 3), (8, 0), (8, 1), (8, 2), (8, 3), (9, 1), (9, 2), (9, 3), (10, 0), (10, 1), (10, 2), (10, 3), (11, 0), (11, 1), (11, 2), (11, 3), (12, 0), (12, 1), (12, 2), (12, 3)]
tops = utils.get_cards_of_rank(4) \
        + utils.get_cards_of_rank(8) \
        + utils.get_cards_of_rank(9) \
        + utils.get_cards_of_rank(10) \
        + utils.get_cards_of_rank(11) \
        + utils.get_cards_of_rank(12)
print(tops)
top_probs = [(1 if index_to_card[i] in tops else 0) for i in range(NUM_CARDS)]
top_policy = probs_to_policy(top_probs)
print("try", try_monte_carlo(top_policy, 100000), 100000)

def random_walk_monte_carlo():
    WALK_LEN = 1000000
    GAMES_PER_STEP = 100000
    SAVE_INTERVAL = 10

    # cur_probs = top_probs
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
        print("Cur win %:", cur_wins / cur_games * 100)

        # create new probs by randomly flipping a bit (turn a card on/off)
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
