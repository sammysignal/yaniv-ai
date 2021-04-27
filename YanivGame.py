from deck_of_cards import deck_of_cards

from helpers import *

def sort_by_rank(card):
    return card.rank

def sort_hand(hand):
    hand.sort(key=lambda c: c.rank)


# Two-player yaniv. This class controls the state of the game. play.py decides which turns to make
class YanivGame:

    def __init__(self):
        # Hands
        self.handOne = []
        self.handTwo = []

        # player 1 = 0, player 2 = 1
        # Left of the dealer goes first
        self.turn = 1

        # The open cards which have been thrown, front cards are most recent
        self.open = []

        # The top card(s) on the open list
        self.top = []

        # Shuffle a new deck of cards
        self.deck = deck_of_cards.DeckOfCards().shuffle_deck()

        # Deal 7 cards
        for i in range(7):
            self.handTwo.append(self.deck.pop(0))
            self.handOne.append(self.deck.pop(0))

        # sort the hands
        sort_hand(self.handOne)
        sort_hand(self.handTwo)

        # Open the top card
        top_card = self.deck.pop(0)
        self.open = [top_card]
        self.top = [top_card]


    def __get_current_hand(self):
        hand = self.handOne
        if (self.turn == 1):
            hand = self.handTwo
        return hand

        
    def make_turn(self, cardsToDrop, pickupFromDeck=False, cardToPickup=None):
        # TODO validate turn
        assert(isinstance(cardsToDrop, list))

        self.open = cardsToDrop + self.open

        # Remove cards from the hand
        hand = self.__get_current_hand()

        for cardToDrop in cardsToDrop:
            for cardInHand in hand:
                if (cardToDrop.suit == cardInHand.suit) and (cardToDrop.rank == cardInHand.rank):
                    hand.remove(cardInHand)
                    break

        # Pickup card
        if (pickupFromDeck):
            # if no more cards, reset the discarded cards
            if len(self.deck) == 0:
                new_deck = deck_of_cards.DeckOfCards()
                new_deck.deck = self.open
                self.deck = new_deck.shuffle_deck()

            hand.append(self.deck.pop(0))
        else:
            hand.append(cardToPickup)

        # update turn
        self.turn = (self.turn + 1) % 2

        # update top cards
        self.top = cardsToDrop

        # sort the hands
        sort_hand(self.handOne)
        sort_hand(self.handTwo)

        return 0


    def show(self):
        # TODO validate turn
        hand_one_sum = get_hand_sum(self.handOne)
        hand_two_sum = get_hand_sum(self.handTwo)

        print("Player 1: " + str(hand_one_sum))
        print("Player 2: " + str(hand_two_sum))

        if (hand_one_sum < hand_two_sum):
            print("Player 1 wins!!")
        elif (hand_one_sum > hand_two_sum):
            print("Player 2 wins!!")
        else:
            if (self.turn == 0):
                print("Player 2 wins!!")
            else:
                print("Player 1 wins!!")


