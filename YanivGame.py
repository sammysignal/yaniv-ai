from deck_of_cards import deck_of_cards

from helpers import print_card_list

def sort_by_rank(card):
    return card.rank

def sort_hand(hand):
    hand.sort(key=lambda c: c.rank)


# Two-player yaniv
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

    def get_hand_sum(self, hand):
        s = 0
        for card in hand:
            s = s + card.value
        return s

        
    def make_turn(self, cardsToDrop, pickupFromDeck=False, cardToPickup=None):
        # TODO validate turn
        assert(isinstance(cardsToDrop, list))
        self.top = cardsToDrop
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
            hand.append(self.deck.pop(0))
        else:
            hand.append(cardToPickup)

        # update turn
        self.turn = (self.turn + 1) % 2

        # sort the hands
        sort_hand(self.handOne)
        sort_hand(self.handTwo)


    def show(self):
        # TODO validate turn
        hand_one_sum = self.get_hand_sum(self.handOne)
        hand_two_sum = self.get_hand_sum(self.handTwo)


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


