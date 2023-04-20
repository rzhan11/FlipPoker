from game_constants import *
import poker_hands
import game
from pretty import card_to_str, hand_to_str
import utils

import random
from heapq import heappop, heappush

def try_monte_carlo(policy, count):
    wins = 0
    for i in range(count):
        res = game.play_game(policy)
        if res > 0:
            wins += 1
    return wins

def probs_to_policy(probs):
    return lambda x, y: probs


def search(initial_policy_count=10, games_per_step=100000, save_interval=10):
    initial_policies = [tuple(random.randint(0, 1) for j in range(NUM_CARDS)) for i in range(initial_policy_count)]

    win_rates = {} # policy: [cur_wins, cur_games]
    policy_heuristics = {} # policy: [neigh_wins, neigh_games]
    last_change = {} # policy: last_change_iter
    queue = [(-1, p, 0) for p in initial_policies]

    num_iter = 0

    while len(queue) > 0:
        print("Step:", num_iter)

        # get state at front of heap
        cur_heur, cur_probs, cur_change_iter = heappop(queue)

        # if it isn't the most recent heur, skip
        if cur_probs in last_change and last_change[cur_probs] != cur_change_iter:
            continue

        # if it has already been played, skip
        if cur_probs in win_rates:
            continue

        # play current state
        cur_cards = [index_to_card[i] for i in range(NUM_CARDS) if cur_probs[i] == 1]
        cur_policy = probs_to_policy(cur_probs)
        cur_wins = try_monte_carlo(cur_policy, games_per_step)

        # update win rates
        win_rates[cur_probs] = [cur_wins, games_per_step]
        print("Cur cards:", cur_cards)
        print("Cur win %:", cur_wins / games_per_step * 100)
        print("---\n")

        # save every 'save_interval' iters
        if num_iter % save_interval == 0:
            print("Saving!")
            with open(f"../data/fixed_heur/step_{num_iter}.txt", "w") as f:
                # print best cards info
                best_probs = None
                best_score = 0
                for p, v in win_rates.items():
                    wr = v[0] / v[1]
                    if wr > best_score:
                        best_probs, best_score = p, wr
                best_cards = [index_to_card[i] for i in range(NUM_CARDS) if best_probs[i] == 1]
                f.write("Best:\n")
                f.write(str(best_cards)+"\n")
                f.write(str(win_rates[best_probs][0] / win_rates[best_probs][1])+"\n")

                # print current cards info
                f.write("Current:\n")
                f.write(str(cur_cards)+"\n")
                f.write(str(cur_heur)+"\n")
                f.write(str(win_rates[cur_probs][0] / win_rates[cur_probs][1])+"\n")

        # iterate through all neighbors
        new_probs = list(cur_probs)
        for i in range(NUM_CARDS):
            # flip bit
            new_probs[i] = 1 - new_probs[i]
            neigh = tuple(new_probs)

            # check to make sure not already played
            if neigh not in win_rates:
                if neigh not in policy_heuristics:
                    policy_heuristics[neigh] = [0, 0]
                policy_heuristics[neigh][0] += cur_wins
                policy_heuristics[neigh][1] += games_per_step
                last_change[neigh] = num_iter

                # add neighbor to queue
                heappush(queue, (- policy_heuristics[neigh][0] / policy_heuristics[neigh][1], neigh, num_iter))

            # flip back
            new_probs[i] = 1 - new_probs[i]

        num_iter += 1


search(games_per_step=1000)
