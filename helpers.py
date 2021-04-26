from deck_of_cards import deck_of_cards


# 0=spades, 1=hearts, 2=diamonds, 3=clubs
SUITS = ["S", "H", "D", "C"]

def card_string(card):
    card_value = card.name.split(' ', 1)[0]
    card_suit = SUITS[card.suit]
    return card_value + " " + card_suit


def print_card_list(hand):
    output = ""
    for i in range(len(hand) - 1):
        output = output + card_string(hand[i]) + " | "
    output = output + card_string(hand[-1])
    print(output)