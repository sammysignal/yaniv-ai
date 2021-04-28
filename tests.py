from deck_of_cards import deck_of_cards

from helpers import *


def get_some_cards():
	return deck_of_cards.DeckOfCards().shuffle_deck()

def test_shorthand():
    deck = deck_of_cards.DeckOfCards().shuffle_deck()
    card_names = [c.name for c in get_cards_by_shorthand(deck, '2c 3d jh')]
    assert(card_names == ['2 of clubs', '3 of diamonds', 'Jack of hearts'])
    return

def test_get_possible_cards_to_drop():
	deck = get_some_cards()
	hand = get_cards_by_shorthand(deck, "AS 2S 3S 3D 4S 10H 10D 10S 10C")

	sort_hand(hand)

	possible_cards_to_drop = get_possible_cards_to_drop(hand)
	possible_shs_to_drop = []
	for droppable in possible_cards_to_drop:
		shorthand_sequence = ' '.join([get_shorthand_for_card(c) for c in droppable])
		possible_shs_to_drop.append(shorthand_sequence)

	assert(len(possible_shs_to_drop) == 24)
	assert('AS 2S 3S 4S' in possible_shs_to_drop)
	assert('AS 2S 3S' in possible_shs_to_drop)
	assert('2S 3S 4S' in possible_shs_to_drop)
	assert('10S 10H' in possible_shs_to_drop)
	assert('10S 10C' in possible_shs_to_drop)
	assert('10S 10H 10D 10C' in possible_shs_to_drop)


def run_tests():
	test_shorthand()
	test_get_possible_cards_to_drop()

if __name__ == '__main__':
	run_tests()
	print("All tests passed.")
