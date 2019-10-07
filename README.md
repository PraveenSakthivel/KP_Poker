# Poker by Praveen Sakthivel

## How to run
- Have python 3 installed on your system
- Run:
 ```
python poker.py
```

## Rules of Poker (Texas hold 'em):
- User starts with a 100 dollars
- User makes a bet or checks, and the cpu matches
- Hands of 2 cards are dealt to all players, 5 cards from deck placed face down in the middle
- For the next 5 rounds bets are placed at the beginning and one card is revealed from the middle each round
- Using the standard rules of texas hold em the hands are evaluated
- If players have the same type of hand, the deck is resolved by high card
- Pot is distrubted accordingly based on the winner
- User can continue to keep playing another round


## Design choices:
- The deck is represented as an array of numbers ranging from 0 - 51
- 0 is the ace of Spades. 1 is the 1 of spades and the deck increases accordingly
- At the end of a suite, the clover suite begins and after that, the heart begins followed by the diamond
- The cards were designed like this to allow for easy identification through the use of modulus and division functions
- All core parts of the game were modularized into their own individual functions to allow for easy readability:
- The get_points method goes and checks through for each of the possible poker hands and adds the value accordingly
- This method is admittedly the least readable function of the code, the various poker hands require a good amount of logic to evaluate
- A better design decision would have been to have create classes for the cards and enumerations for suites and ranks to better improve readability

## Libraries
- This application only makes use of the standard python libraries
