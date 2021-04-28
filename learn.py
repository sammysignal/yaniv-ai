import pickle

from YanivGame import YanivGame
from helpers import *


### This class is responsible for executing a Q-Learning algorithm and devloping a gameplay policy.

# Game state encodes the state of the game right after making your turn.
# 25480
GAME_STATE_KEY_OPTIONS = [
    range(1, 8), # Number of cards in my hand
    range(2),    # 1 indicates sum of cards is more than 20, 0 indicates less than or equal to 20.
    range(20),   # Sum of cards in my hand mod 20 (or 20 if greater than 40)
    range(1, 8), # Number of cards in opponent's hand
    range(1, 14) # Rank of lowest top card that you dropped
]


GAMMA = 0.9
GAMES = 1


values = {}

# Noise represents the probability of making a random move.
def noise(games_played):
    # Linear fraction of games played:  0 -> 1; 50 -> 0.5; 100 -> 0
    return (float(GAMES - games_played) / GAMES)


def get_state_key_for_game(game, cardsToDrop):
    hand = game._get_current_hand()
    hand_count = len(hand)
    hand_sum = get_hand_sum(hand)
    big = 1
    if hand_sum >= 40:
        hand_sum = 20
    elif 20 < hand_sum and hand_sum < 40:
        hand_sum = hand_sum % 20
    else: # if hand_sum <= 20
        big = 0

    opponent_hand = game._get_opponent_hand()
    opponent_hand_count = len(opponent_hand)

    minimum_dropped_rank = min([c.rank for c in cardsToDrop])

    keys = [str(hand_count), str(big), str(hand_sum), str(opponent_hand_count), str(minimum_dropped_rank)]

    return keys.join('_')

def initialize_state():
    for a in GAME_STATE_KEY_OPTIONS[0]:
        for b in GAME_STATE_KEY_OPTIONS[1]:
            for c in GAME_STATE_KEY_OPTIONS[2]:
                for d in GAME_STATE_KEY_OPTIONS[3]:
                    for e in GAME_STATE_KEY_OPTIONS[4]:
                        key = '_'.join([str(a), str(b), str(c), str(d), str(e)])
                        values[key] = 0



def get_value(game):
    # execute a policy based on the values and gamma
    # set this new value and recurse on the next value
    # V = Max(current reward + gamma*Sum(over each P(next state given current state)*V(next state)))

    hand = game._get_current_hand()

    # List of lists
    possible_cards_to_drop = get_possible_cards_to_drop(hand)



def main():
    # Initialize all values to zero
    initialize_state()

    print("Initialized values to zero.")
    print("Values size is " + str(len(values)))

    # while true
        # get starting value (which also plays a game out)
        # tick gamma
    i = 0
    while i < GAMES:
        game = YanivGame()
        get_value(game)
        i = i + 1



if __name__ == '__main__':
    main()
