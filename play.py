# External imports
from deck_of_cards import deck_of_cards

# Local imports
from YanivGame import YanivGame
from helpers import print_card_list, SUITS




# solve for  the fact that ten of spades needs to be two letters, so 1S instead of 10S
def get_card_code(card_nickname):
    if len(card_nickname) == 3 and card_nickname[0:2] == '10':
        return '1' + card_nickname[2]
    return card_nickname

def get_shorthand_for_card(card):
    card_value_initial = card.name.split(' ', 1)[0][0]
    card_suit = SUITS[card.suit]
    return card_value_initial + card_suit

def get_cards_by_shorthand(hand, shorthand):
    # e.g., shortand = 7D, or shorthand = 7D KS (for multiple cards)
    cards = []
    card_nicknames = shorthand.split(' ')
    for card_nickname in card_nicknames:
        for card in hand:
            if get_shorthand_for_card(card) == get_card_code(card_nickname).upper():
                cards.append(card)
                break

    return cards

def make_computer_turn(game):
    print("making computer turn:")
    game.make_turn([game.handOne[0]], True)
    return False

def make_human_turn(game):
    hand = game.handTwo

    print("your hand:")
    print_card_list(hand)

    print("top cards:")
    print_card_list(game.top)


    hand_sum = game.get_hand_sum(hand)

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
            break

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

