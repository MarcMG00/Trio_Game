class Card:
    def __init__(self, value: int):
        self.value = value
        self.revealed = False
        self.discarded = False

    def reveal(self):
        self.revealed = True

    def hide(self):
        self.revealed = False

    # Discard card when the trio is completed
    def discard(self):
        self.discarded = True # to see it as "D"
        self.revealed = True

    def __str__(self):
        if self.discarded:
            return " D"
        if self.revealed:
            return f"{self.value:>2}"
        return " X"