# yaniv-ai
An AI built in python that learns to play the card game, Yaniv.

## Approach
This implementation uses Q-Learning to gradually learn to play Yaniv by forcing the model to play itself repeatedly. This might be described as a monte-carlo learning track, since we only update the Q-value if the game has reached that state before. The hope is that this makes training faster, though not as robust.

The current implementation has a state size of `168`, but increasing this value by making the state more specific will likely make the model more robust.

## Usage

```
$ python learn.py <flag>

Flags:
       learn:      Start learning
       continue n: Continue learning with an additional n games
       play:       Play against the trained model
```

## Dependencies

 ```
 pip3 install deck_of_cards
 ```

## Files

 - `learn.py`
   - Trains a Q-Learning algorithm to play Yaniv. The Q-Values are stored in
 - `YanivGame.py`
   - The Class containing all the information about a single game of Yaniv.
 - `play.py`
   - functions that provide user interface for playing the game against a computer
 - `helpers.py`
   - Static helper functions
 - `tests.py`
   - Some simple tests for the helpers
 - `Q_Values.p`
   - Contains the model

## Rules of the Game

There are many different ways to play this game, but the version implemented here is a two-player implementation with the following rules:

 - Two players are each dealt 7 cards
 - Players take turns
 - On each turn, a player must discard one or more cards, then pick up one card.
   - The discarded cards must be either (a) pairs of two or more, or (b) suited sequences of three or more.
   - After discarding card(s) the player can either pickup one card from the top of the discard pile (choosing among any of the most recently discarded cards) or the player can pickup one card from the top of the deck
 - If at the beginning of the turn a player has cards that sum to a value less than or equal to 7, the player may elect to 'show' their cards, in which case both players show their cards.
   - If the sum of the opponent's hand is less than or equal to the sum of the player's hand, the opponent wins. Otherwise, the player wins.
