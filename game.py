from deck import Deck
from player import Player

class Game:
    def __init__(self, nb_players: int):
        self.deck = Deck()
        self.cards_on_table = []
        self.players = [Player(i + 1) for i in range(nb_players)]
        self.current_player_index = 0

        self.nb_cards_player = 0
        self.nb_cards_on_table = 0
        self.set_nb_cards_on_game(nb_players)

    # Set the number of cards to deal on players and to put on the table
    def set_nb_cards_on_game(self, nb_players: int):
        if nb_players == 3:
            self.nb_cards_player = 9
            self.nb_cards_on_table = 9
        elif nb_players == 4:
            self.nb_cards_player = 7
            self.nb_cards_on_table = 8
        elif nb_players == 5:
            self.nb_cards_player = 6
            self.nb_cards_on_table = 6
        else:
            self.nb_cards_player = 5
            self.nb_cards_on_table = 6

    # Prepare the game
    def setup(self):
        # Put Cards for players
        for player in self.players:
            player.deal_cards(self.deck, self.nb_cards_player)

       # Put Cards on table
        self.cards_on_table = [self.deck.draw() for _ in range(self.nb_cards_on_table)]

    # Show Cards on table
    def display_cards_on_table(self):
        for player in self.players:
            player.display()

    # Start of the game
    def play(self):
        print("\nComienza la partida")