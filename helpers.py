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

# e.g. {King of Spades} -> KS ;  {10 of Hearts} -> 10S
def get_shorthand_for_card(card):
    assert(isinstance(card, deck_of_cards.Card))

    rank_name = ''
    if 2 <= card.rank and card.rank <= 10:
        rank_name = str(card.rank)
    else:
        rank_name = card.name.split(' ', 1)[0][0]

    suit = SUITS[card.suit]

    return rank_name + suit

def get_cards_by_shorthand(hand, shs):
    # e.g., shortand = 7D, or shorthand = 7D KS (for multiple cards)
    cards = []
    sh_list = shs.split(' ')
    for sh in sh_list:
        for card in hand:
            if get_shorthand_for_card(card) == sh.upper():
                cards.append(card)
                break

    if len(sh_list) == len(cards):
        return cards
    return []

def validate_cards_to_drop(cards):
    n = len(cards)
    if n <= 1:
        return bool(n)

    # First let's check if all cards have the same rank
    first_rank = cards[0].rank
    all_cards_same = all([card.rank==first_rank for card in cards])
    if (all_cards_same):
        return True

    # Now let's check for sequences
    if n <= 2:
        return False

    cards_sorted = sorted(cards, key=lambda c: c.rank)
    first_suit = cards[0].suit
    for i in range(n):
        # rank must increase and suit must stay the same
        if (cards_sorted[i].rank == first_rank + i) and (cards_sorted[i].suit == first_suit):
            continue
        else:
            return False
    
    return True

def get_hand_sum(hand):
    s = 0
    for card in hand:
        s = s + card.value
    return s


def test_helpers():
    pass


if __name__ == '__main__':
    test_helpers()
