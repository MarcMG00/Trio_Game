class Player:

    def __init__(self, number: int):
        self.number = number
        self.cards = []
        self.nb_trios = 0
        self.has_scored_current_turn = False
        self.is_winner = False

    # Distribute a number of Cards depending on number of players
    def deal_cards(self, deck, nbCards : int):
        for _ in range(nbCards):
            self.cards.append(deck.draw())

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
        self.cards.sort(key=lambda x: x.value)

    # Show own Cards to player
    def display_own_cards(self):
        print("Cartas : ")

        # Filters Cards not discarded
        available_cards = [c for c in self.cards if not c.discarded]
        for card in available_cards:
            card.reveal

        print(" | ".join(str(card.value) for card in available_cards))

    # Hide own Cards to player
    def hide_own_cards(self):
        # Filters Cards not discarded
        available_cards = [c for c in self.cards if not c.discarded]
        available_cards = [c.hide for c in available_cards]

        row_str = " | ".join(str(card.value) for card in available_cards)
        print(f"{row_str}")
        