class Player:

    def __init__(self, number: int):
        self.number = number
        self.cards = []
        self.nbTrios = 0
        self.isWinner = False

    # Distribute a number of Cards depending on number of players
    def deal_cards(self, deck, nbCards : int):
        for _ in range(nbCards):
            card = deck.draw()
            card.reveal
            self.cards.append(card)

    # Reveal Card (show the lower:1 or the higher:2)
    def reveal_card(self, position_card: int):
        # Filters Cards not discarded
        available_cards = [c for c in self.cards if not c.discarded]

        if position_card == 1:
            available_cards[-1].reveal()
        else:
            available_cards[0].reveal()

    # Reorder Cards in ascending order
    def reorder_cards(self):
        self.cards.sort(key=lambda x: x.value, reverse=False)