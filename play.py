# External imports
from deck_of_cards import deck_of_cards

# Local imports
from YanivGame import YanivGame
from helpers import *


def make_computer_turn(game):
    print("making computer turn:")
    game.make_turn([game.handOne[-1]], True)
    return False

def make_human_turn(game):
    hand = game.handTwo

    print("your hand:")
    print_card_list(hand)

    print("top cards:")
    print_card_list(game.top)

    hand_sum = get_hand_sum(hand)

    if (hand_sum <= 7):
        show_string = input("Show? (y/n): ")
        while not (show_string == 'y' or show_string == 'n'):
            show_string = input("Show? (y/n): ")
        if (show_string == 'y'):
            game.show()
            return True

    cards_to_drop = []
    while (True):
        drop_string = input("Choose card(s) to drop: ")
        cards_to_drop = get_cards_by_shorthand(hand, drop_string)
        if not cards_to_drop == []:
            if (validate_cards_to_drop(cards_to_drop)):
                break
            print("Invalid set of cards to drop.")

    cards_to_pickup = []
    pickup_string = ''
    while (True):
        pickup_string = input("Choose card to pickup (or enter to draw from the top of the deck): ")
        if (pickup_string == ''):
            break
        cards_to_pickup = get_cards_by_shorthand(game.top, pickup_string)
        if not cards_to_pickup == []:
            break

    if cards_to_pickup == []:
        game.make_turn(cards_to_drop, True)
    else:
        game.make_turn(cards_to_drop, False, cards_to_pickup[0])

    return False

def main():
    game = YanivGame()

    # human is player 2, they go first.
    done = make_human_turn(game)
    while (done == False):
        if (game.turn == 0):
            done = make_computer_turn(game)
        else:
            done = make_human_turn(game)


if __name__ == "__main__":
    main()

