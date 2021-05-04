import pickle, random, sys
from deck_of_cards import deck_of_cards

from YanivGame import YanivGame
from helpers import *


### This class is responsible for executing a Q-Learning algorithm and devloping a gameplay policy.

###  Run formats  ###
## python learn.py learn
#    - start learning, learn default number of games
#
## python learn.py continue 100
#    - continue learning where it left off, with the number of games to learn
#
## python learn.py play
#    - Play against the trained model
#

values = {}

PICKLE_FILE = "Q_Values.p"


# Game state encodes the state of the game right after making your turn.
# State dimenstions to consider in the future:
#   - Number of cards in opponent's hand
# 7280
GAME_STATE_KEY_OPTIONS = [
    range(1, 8),  # number of cards in hand
    range(1, 13), # Sum group of cards in my hand (1,2,3,4,5,6,7,8-9,10-12,13-16,17-25,26+)
    range(2),     # Did we show our cards this turn
]

GAMMA = 0.99
LEARNING_RATE = 0.1

# Default games to learn
GAMES = 10

class SAR:
    # Define an action on a hand. Defaults to picking up from the top of the deck.
    def __init__(self, expected_value, hand, dropped_cards, pickup_from_deck=True, card_to_pickup_from_top=None, show=False):
        # S
        self.hand = hand
        self.dropped_cards = dropped_cards

        # A
        self.pickup_from_deck = pickup_from_deck
        self.card_to_pickup_from_top = card_to_pickup_from_top
        self.show = show

        # R/V
        self.expected_value = expected_value

def set_key_value(key, value):
    global values
    if value > 0.001:
        print("setting key: " + key + " with value: " + str(value))
    values[key] = value

# y = (-1/(games/2)) *x + 1
# y = 1 - x(2/games)
def noise(games_played):
    """
    Noise represents the probability of making a random move.
    """
    # Linear fraction of games played:  0 -> 1; 50 -> 0.5; 100 -> 0
    #       return (float(GAMES - games_played) / GAMES)

    # 100% decreasing to 0% at half games played, then the rest is zero
    half = GAMES/2
    if games_played > half:
        return 0
    return 1 - games_played*(float(2)/GAMES)

def initialize_state():
    global values
    """
    Initialize state dictionary to zero (or custom values)
    """
    for a in GAME_STATE_KEY_OPTIONS[0]:
        for b in GAME_STATE_KEY_OPTIONS[1]:
            for c in GAME_STATE_KEY_OPTIONS[2]:
                key = '_'.join([str(a), str(b), str(c)])

                # # Initialize values to something very close to 0 so that the initial algorithm favors hands
                # # of low sum. This minor intervention will dramatically speed up the training process.
                # values[key] = 0.1*(float(1-b)*0.1 + float(20-c)*0.001 + 0.0001)

                # # Initialize values to something very close to zero but favoring less cards
                # values[key] = 0.01 * (1 - (float(a) / 7))

                # Initialize to zero
                values[key] = 0

def get_state_key_for_game(hand, show=True):
    hand_count = len(hand)
    hand_sum = get_hand_sum(hand)
    sum_denomination = get_sum_denomination(hand_sum)

    # minimum_dropped_rank = min([c.rank for c in cardsToDrop])

    show_int = int(show)

    keys = [str(hand_count), str(sum_denomination), str(show_int)]

    return '_'.join(keys)


# Future states includes all possible cards to be picked up from the top or the the deck, but only gives expectation
# for state after picking up from deck.
def get_possible_actions(game):
    global values

    hand = game._get_current_hand()
    top_cards = game.top

    # List of lists
    possible_cards_to_drop = get_possible_cards_to_drop(hand)

    sars = []

    if get_hand_sum(hand) <= 7:
        state_key = get_state_key_for_game(hand)
        # expected_value, hand, dropped_cards, pickup_from_deck=True, card_to_pickup_from_top=None, show=False
        sar_show = SAR(values[state_key], hand, [], False, None, True)
        sars.append(sar_show)

    ## Check normal moves
    for cards_to_drop in possible_cards_to_drop:
        hand_after_drop = list(filter(lambda x: x not in cards_to_drop, hand))
        # SARs for pickup from deck
        # for rank in range(1, 14):
        #     for suit in range(4):

        # Actually, we only want to consider SARs for the actions we have control over.
        # In this case, that means all of the possible cards we could pick up should be part
        #   of a single action piece - namely, picking up from the deck.

        # hand_after_pickup = list(hand_after_drop) + [card_to_pickup_from_deck]
        # state_key = get_state_key_for_game(hand, cards_to_drop, False)

        sum_of_deck_values = 0
        # Get value for every possible card you could pick up from the deck, then use that to calculate
        # The overall expected value
        d = deck_of_cards.DeckOfCards().deck
        # TODO: should we count cards? (exclude cards in top?) for now, no.
        for c in d:
            hand_after_pickup = hand_after_drop + [c]
            deck_card_key = get_state_key_for_game(hand_after_pickup, False)
            deck_card_value = values[deck_card_key]
            sum_of_deck_values = sum_of_deck_values + deck_card_value

        expected_value = sum_of_deck_values / 52 # average value of all possible cards you could pick up from deck
        # expected_value, hand, dropped_cards, pickup_from_deck=True, card_to_pickup_from_top=None, show=False
        sar = SAR(expected_value, hand, cards_to_drop, True, None, False)
        sars.append(sar)

        # SARs for pickup from top
        for card in top_cards:
            # hand_after_drop = filter(lambda x: x not in cards_to_drop, hand)

            hand_after_pickup = list(hand_after_drop) + [card]
            state_key = get_state_key_for_game(hand_after_pickup, False)
            expected_value = 1 * values[state_key]
            # expected_value, hand, dropped_cards, pickup_from_deck=True, card_to_pickup_from_top=None, show=False
            sar = SAR(expected_value, hand, cards_to_drop, True, card, False)
            sars.append(sar)


    return sars



def make_move_and_learn(game, games_played):
    global values

    # execute a policy based on the values and gamma
    # V = Max(current reward + gamma*Sum(over each P(next state given current state)*V(next state)))
    # V = Max_a(gamma*Sum(over each P(next state given current state)*V(next state)))


    # hand, dropped_cards, pickup_from_deck, card_to_pickup_from_top, show, expected_value
    sars = get_possible_actions(game)

    probability_of_random_move = noise(games_played)

    # # The move made is not necessarily the best move. It will be the same unless noise is applied.
    # if random.random() < noise:
    #     move_sar = random.choice(sars)

    #     game.make_turn(move_sar.dropped_cards, move_sar.pickup_from_deck, move_sar.card_to_pickup_from_top)

    current_hand = game._get_current_hand()

    best_action = random.choice(sars)
    if random.random() > probability_of_random_move:
        # If we're not doing a random move, find the best move.
        largest_expected_value = 0
        for sar in sars:
            # hand, dropped_cards, pickup_from_deck, card_to_pickup_from_top, show, expected_value
            if (sar.expected_value > largest_expected_value):
                best_action = sar
                largest_expected_value = sar.expected_value

    if best_action.show:
        winner = game.show()
        if winner == game.turn + 1:
            # we will have won
            key = get_state_key_for_game(current_hand)
            old_value = values[key]

            # !!!! Do the thing !!!!
            new_value = old_value + LEARNING_RATE*(GAMMA*1 - old_value)
            set_key_value(key, new_value)

        return

    # Make move and learn:
    key = get_state_key_for_game(current_hand, False)
    old_value = values[key]

    # !!!! Do the thing !!!!
    new_value = old_value + LEARNING_RATE*(GAMMA*best_action.expected_value - old_value)
    set_key_value(key, new_value)

    if best_action.pickup_from_deck:
        game.make_turn(best_action.dropped_cards)
    else:
        game.make_turn(best_action.dropped_cards, best_action.pickup_from_deck, best_action.card_to_pickup)

    # Recurse
    make_move_and_learn(game, games_played)

def learn(games_to_play=GAMES, start=True):
    global values

    if start:
        # Initialize all values to zero
        initialize_state()
    else:
        # If continuation, load pickle file into values
        values = pickle.load(open(PICKLE_FILE, "rb" ))

    print("Initialized values to zero.")
    print("Values size is " + str(len(values)))

    i = 0
    while i < games_to_play:
        game = YanivGame()
        make_move_and_learn(game, i)
        i = i + 1

    # Write dictionary to a pickle file
    pickle.dump(values, open(PICKLE_FILE, "wb" ))


def print_usage():
    print("Usage: python learn.py <flag>")
    print("Flags:")
    print("       learn:      Start learning")
    print("       continue n: Continue learning with an additional n games")
    print("       play:       Play against the trained model")

if __name__ == '__main__':
    ## python learn.py learn
    #    - start learning, learn default number of games

    ## python learn.py continue 100
    #    - continue learning where it left off, with the number of games to learn

    ## python learn.py play
    #    - Play against the trained model
    if len(sys.argv) >= 2:
        flag = sys.argv[1]
        if flag == "learn":
            learn()
        elif flag == "continue":
            n_games = int(sys.argv[2])
            learn(n_games, False)
        elif flag == "play":
            print("Not implemented")
        else:
            print_usage()
    else:
        print_usage()

            
