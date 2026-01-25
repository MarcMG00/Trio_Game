import random
from card import Card

class Deck:
    def __init__(self):
        self.cards = []
        self._build()
        self.shuffle()

    # Set initial deck of the game
    def _build(self):
        # Original deck for Trio game
        values = (
            [1] * 3 +
            [2] * 3 +
            [3] * 3 +
            [4] * 3 +
            [5] * 3 +
            [6] * 3 +
            [7] * 3 +
            [8] * 3 +
            [9] * 3 +
            [10] * 3 +
            [11] * 3 +
            [12] * 3
        )

        for v in values:
            self.cards.append(Card(v))

    # Shuffle deck
    def shuffle(self):
        random.shuffle(self.cards)

    # Get Card from above of the deck
    def draw(self):
        return self.cards.pop()