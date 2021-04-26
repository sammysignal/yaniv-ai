from deck_of_cards import deck_of_cards

from play import get_cards_by_shorthand


def test_shorthand():
    deck = deck_of_cards.DeckOfCards().shuffle_deck()
    card_names = [c.name for c in get_cards_by_shorthand(deck, '2c 3d jh')]
    assert(card_names == ['2 of clubs', '3 of diamonds', 'Jack of hearts'])
    return


def run_tests():
	test_shorthand()

if __name__ == '__main__':
	run_tests()
	print("All tests passed.")