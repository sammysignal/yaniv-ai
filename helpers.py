import copy
from itertools import combinations, chain
from deck_of_cards import deck_of_cards


# 0=spades, 1=hearts, 2=diamonds, 3=clubs
SUITS = ["S", "H", "D", "C"]

def sort_by_rank(card):
    return (100*card.rank) + card.suit

def sort_hand(hand):
    hand.sort(key=sort_by_rank)

def powerset(iterable, min_size):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(min_size, len(s)+1))

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

# get all contiguous subsequences, from: https://stackoverflow.com/questions/41576911/list-all-contiguous-sub-arrays
# size at least 3
def get_possible_subsequences(L):
    result = []
    for w in range(1, len(L)+1):
        for i in range(len(L)-w+1):
            if (i+w - i >= 3):
                result.append(L[i:i+w])
    return result


def get_possible_cards_to_drop(hand):
    cards_to_drop = [[c] for c in hand]

    # [spades, hearts, diamonds, clubs]

    # Check for sequences
    for s in range(4):
        current_sequence = []
        previous_card = None
        found_previous_card = False
        for rank_minus_one in range(13):
            card = None
            found_card = False
            for c in hand:
                if c.rank == rank_minus_one + 1 and c.suit == s:
                    found_card = True
                    card = c
                    break

            if not found_card:
                continue

            if rank_minus_one > 0 and found_previous_card and card.rank == previous_card.rank + 1 and card.suit == previous_card.suit:
                current_sequence.append(card)
            else:
                if (len(current_sequence) >= 3):
                    subsequences = get_possible_subsequences(current_sequence)
                    cards_to_drop = cards_to_drop + subsequences
                current_sequence = [card]

            found_previous_card = True
            previous_card = card
    
        if (len(current_sequence) >= 3):
            subsequences = get_possible_subsequences(current_sequence)
            cards_to_drop = cards_to_drop + subsequences

    # Check for pairs
    for rank_minus_one in range(13):
        current_pair = []
        previous_card = None
        found_previous_card = False
        for s in range(4):
            card = None
            found_card = False
            for c in hand:
                if c.rank == rank_minus_one + 1 and c.suit == s:
                    found_card = True
                    card = c
                    break

            if not found_card:
                continue

            if rank_minus_one > 0 and found_previous_card and card.rank == previous_card.rank:
                current_pair.append(card)
            else:
                if (len(current_pair) >= 2):
                    all_combinations = powerset(current_pair, 2)
                    for combo in all_combinations:
                        cards_to_drop.append(list(combo))
                current_pair = [card]

            found_previous_card = True
            previous_card = card
    
        if (len(current_pair) >= 2):
            all_combinations = powerset(current_pair, 2)
            for combo in all_combinations:
                cards_to_drop.append(list(combo))


    return cards_to_drop




def get_hand_sum(hand):
    s = 0
    for card in hand:
        s = s + card.value
    return s

