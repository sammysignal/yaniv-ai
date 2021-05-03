import pickle, random
from deck_of_cards import deck_of_cards

from YanivGame import YanivGame
from helpers import *


### This class is responsible for executing a Q-Learning algorithm and devloping a gameplay policy.

# Game state encodes the state of the game right after making your turn.
# State dimenstions to consider in the future:
#   - Number of cards in opponent's hand
# 7280
GAME_STATE_KEY_OPTIONS = [
    range(1, 8),  # Number of cards in my hand
    range(2),     # 1 indicates sum of cards is more than 20, 0 indicates less than or equal to 20.
    range(20),    # Sum of cards in my hand mod 20 (or 19 if greater than 39)
    range(1, 14), # Rank of lowest top card that you dropped
    range(2),     # Did we show our cards this turn
]

GAMMA = 0.99
LEARNING_RATE = 0.1

GAMES = 1


values = {}

class SAR:
    def __init__(self, hand, dropped_cards, pickup_from_deck, card_to_pickup, show, expected_value):
        # S
        self.hand = hand
        self.dropped_cards = dropped_cards

        # A
        self.pickup_from_deck = pickup_from_deck
        self.card_to_pickup = card_to_pickup
        self.show = show

        # R/V
        self.expected_value = expected_value

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
    """
    Initialize state dictionary to zero (or custom values)
    """
    for a in GAME_STATE_KEY_OPTIONS[0]:
        for b in GAME_STATE_KEY_OPTIONS[1]:
            for c in GAME_STATE_KEY_OPTIONS[2]:
                for d in GAME_STATE_KEY_OPTIONS[3]:
                    for e in GAME_STATE_KEY_OPTIONS[4]:
                        key = '_'.join([str(a), str(b), str(c), str(d), str(e)])

                        # Initialize values to something very close to 0 so that the initial algorithm favors hands
                        # of low sum. This minor intervention will dramatically speed up the training process.
                        values[key] = 0.1*(float(1-b)*0.1 + float(20-c)*0.001 + 0.0001)

def get_state_key_for_game(hand, cardsToDrop=None, show=True):
    hand_count = len(hand)
    hand_sum = get_hand_sum(hand)
    big = 1
    if hand_sum >= 39:
        hand_sum = 19
    elif 19 < hand_sum and hand_sum < 39:
        hand_sum = hand_sum % 20
    else: # if hand_sum <= 20
        big = 0

    minimum_dropped_rank = min([c.rank for c in cardsToDrop])

    show_int = int(show)

    keys = [str(hand_count), str(big), str(hand_sum), str(minimum_dropped_rank), str(show_int)]

    return '_'.join(keys)


# Future states includes all possible cards to be picked up from the top or the the deck, but only gives expectation
# for state after picking up from deck.
def get_possible_future_states(game):
    hand = game._get_current_hand()
    top_cards = game.top

    # List of lists
    possible_cards_to_drop = get_possible_cards_to_drop(hand)

    sars = []

    if get_hand_sum(hand) <= 7:
        sar_show = SAR(hand, [], [], True, expected_value)

    ## Check normal moves
    for cards_to_drop in possible_cards_to_drop:
        hand_after_drop = filter(lambda x: x not in cards_to_drop, hand)
        # SARs for pickup from deck
        for rank in range(1, 14):
            for suit in range(4):
                # TODO: should we count cards? (exclude cards in top?) for now, no.
                # hand_after_drop = filter(lambda x: x not in cards_to_drop, hand)

                card_to_pickup_from_deck = deck_of_cards.Card((suit, rank))
                hand_after_pickup = list(hand_after_drop) + [card_to_pickup_from_deck]
                state_key = get_state_key_for_game(hand, cards_to_drop, False)
                expected_value = (values[state_key] / 13.0) # 1/13 chance of getting this card from the deck
                sar = SAR(hand, cards_to_drop, True, card_to_pickup_from_deck, False, expected_value)
                sars.append(sar)

        # SARs for pickup from top
        for card in top_cards:
            # hand_after_drop = filter(lambda x: x not in cards_to_drop, hand)

            hand_after_pickup = list(hand_after_drop) + [card]
            state_key = get_state_key_for_game(hand, cards_to_drop, False)
            expected_value = 1 * values[state_key]
            # hand, dropped_cards, pickup_from_deck, card_to_pickup, show, expected_value
            sar = SAR(hand, cards_to_drop, False, card, False, expected_value)
            sars.append(sar)


    return sars



def make_move_and_learn(game, games_played):
    # execute a policy based on the values and gamma
    # V = Max(current reward + gamma*Sum(over each P(next state given current state)*V(next state)))
    # V = Max_a(gamma*Sum(over each P(next state given current state)*V(next state)))


    # hand, dropped_cards, pickup_from_deck, card_to_pickup_from_top, show, expected_value
    sars = get_possible_future_states(game)
    print(sars)
    return

    probability_of_random_move = noise(games_played)

    # # The move made is not necessarily the best move. It will be the same unless noise is applied.
    # if random.random() < noise:
    #     move_sar = random.choice(sars)

    #     game.make_turn(move_sar.dropped_cards, move_sar.pickup_from_deck, move_sar.card_to_pickup_from_top)

    current_hand = game._get_current_hand()

    best_future_state = None
    largest_expected_value = 0
    for sar in sars:
        # hand, dropped_cards, pickup_from_deck, card_to_pickup_from_top, show, expected_value
        if (sar.expected_value > largest_expected_value):
            best_future_state = sar
            largest_expected_value = sar.expected_value


    # max_future_expected_value = 0

    if best_future_state.show:
        winner = game.show()
        if winner == game.turn + 1:
            # we will have won
            key = get_state_key_for_game(current_hand)
            old_value = values[key]

            # !!!! Do the thing !!!!
            values[key] = old_value + LEARNING_RATE*(GAMMA*1 - old_value)
        return

    # Make move and learn:
    key = get_state_key_for_game(current_hand, best_future_state.dropped_cards, False)
    old_value = values[key]

    # !!!! Do the thing !!!!
    values[key] = old_value + LEARNING_RATE*(GAMMA*best_future_state.expected_value - old_value)

    game.make_turn(best_future_state.dropped_cards, best_future_state.pickup_from_deck, best_future_state.card_to_pickup)

    # Recurse
    make_move_and_learn(game, games_played)

def main():
    # Initialize all values to zero
    initialize_state()

    print("Initialized values to zero.")
    print("Values size is " + str(len(values)))

    # while true
        # get starting value (which also plays a game out)
        # tick
    i = 0
    while i < GAMES:
        game = YanivGame()
        make_move_and_learn(game, i)
        i = i + 1


if __name__ == '__main__':
    main()
