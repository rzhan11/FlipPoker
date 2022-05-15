import json
import matplotlib.pyplot as plt

from game_constants import *
import poker_hands
import game
from pretty import card_to_str, hand_to_str

hand = [0, 4, 8, 12, 17, 48]
cards = [index_to_card[c] for c in hand]
print(cards)
score, poker_hand = poker_hands.get_best_poker_hand(hand)
print("Score:", score)
print("Type:", priority_to_hand_name[score[0]])
print("Poker hand:", hand_to_str(poker_hand))

def get_wants(player_hand, dealer_hand):
    return [0.5] * 52

all_wins = []
num_games = 100000

probs = [i / 100 for i in range(0, 100 + 1)]

for p in probs:
    wins = 0
    for i in range(num_games):
        res = game.play_game(lambda a, b : [p] * 52)
        if res > 0:
            wins += 1
            # print("I won")
        else:
            # print("I lost")
            pass
        # print("---")
    print("p =", p, "won", wins, "out of", num_games)
    all_wins += [wins]

print(all_wins)
with open("../data/wins.json", "w") as f:
    json.dump(all_wins, f)


ratio = [w/num_games for w in all_wins]
xs = [p * 100 for p in probs]
plt.bar(xs, ratio)
plt.savefig("../data/wins.png")
