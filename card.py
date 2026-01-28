class Card:
    def __init__(self, value: int):
        self.value = value
        self.revealed = False
        self.discarded = False
        self.already_taken_by_player = False # allows to not to show the same Card (for option 3) when fliping own Cards)

    def reveal(self):
        self.revealed = True

    def hide(self):
        self.revealed = False
        self.already_taken_by_player = False

    # Discard card when the trio is completed
    def discard(self):
        self.discarded = True # to see it as "D"
        self.revealed = True

    def taken(self):
        self.already_taken_by_player = True

    def __str__(self):
        if self.discarded:
            return "D"
        if self.revealed:
            return f"{self.value:>2}"
        return "X"