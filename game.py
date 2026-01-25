from deck import Deck
from player import Player

class Game:
    def __init__(self, nb_players: int):
        self.deck = Deck()
        self.cards_on_table = []
        self.players = [Player(i + 1) for i in range(nb_players)]
        self.current_player_index = 0
        self.numbers_revealed_on_current_turn = []

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
            player.reorder_cards()

       # Put Cards on table
        self.cards_on_table = [self.deck.draw() for _ in range(self.nb_cards_on_table)]

    # Start of the game
    def play(self):
        print("\nComienza la partida")

        while True:
            # Game ends when a player is winner (has 3 trios or 1 trio of 7s)
            if any(player.is_winner for player in self.players):
                print("\nFin de la partida -- TODO >>> jugador X ganó la partida")
                return

            self.play_turn()

    # Start turns
    def play_turn(self):
        current_player = self.players[self.current_player_index]
        print(f"\nTurno del Jugador {current_player.number}")

        # Show Cards of current player
        current_player.display_own_cards()

        # Continue turn until 2-3 Cards are not the same
        while True:
            print("\nElige una acción :")
            print("1 - Girar una carta del centro")
            print("2 - Pedir una carta a otro jugador")
            print("3 - Girar una carta propia")

            choice = input("Opción: ")

            if choice == "1":
                self.flip_card_on_table()
            elif choice == "2":
                print("2 - TODO")
            elif choice == "3":
                print("3 - TODO")
            else:
                print("Opción inválida.")

            # Check if current Cards revealed allows to player to get a Trio
            self.player_got_trio(current_player)

            # Turn ends if current player hasn't got same numbers when choosing OR if has scored
            if self.has_same_numbers(current_player) is False or current_player.has_scored_current_turn:
                self.hide_cards_on_table()
                break

        # Next player
        self.next_player()

    # Pass to next player (next index)
    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    # Option 1 - Flip a Card from table
    def flip_card_on_table(self):
        print("Elige una posición :")
        index_card = self.ask_position(self.cards_on_table)

        card_to_reveal = self.cards_on_table[index_card]
        self.numbers_revealed_on_current_turn.append(card_to_reveal.value)

        # Show again all Cards on table
        card_to_reveal.reveal()
        available_cards = [c for c in self.cards_on_table if not c.discarded]
        row_str = " | ".join(str(card) for card in available_cards)
        print(f"{row_str}")

        return

    # Check if numbers revealed during current turn are the same
    def has_same_numbers(self, player) -> bool:
        # Set removes duplicateds letting only one number => so if there are 2 numbers and returns 1, it means that those numbers are the same
        all_same  = len(set(self.numbers_revealed_on_current_turn)) == 1

        # Set player has score if 3 Cards are the same
        if len(self.numbers_revealed_on_current_turn) == 3 and all_same:
            player.has_scored_current_turn = True
            return True

        # Otherwise, returns if current list has the same numbers
        return all_same
    
    # Set if player got a trio of numbers
    def player_got_trio(self, player):
        # Set player has score if 3 Cards are the same
        if self.has_same_numbers(player) and len(self.numbers_revealed_on_current_turn) == 3:
            player.nb_trios += 1
            player.has_scored_current_turn = True

    # Get Card asked from table
    def ask_position(self, cards_list):
        # Filters Cards not discarded
        available_cards = [c for c in cards_list if not c.discarded]
        row_str = " | ".join(str(card) for card in available_cards)
        print(f"{row_str}")

        while True:
            try:
                index_card = int(input("Posición de la carta :")) - 1

                if not (0 <= index_card < len(available_cards)):
                    print(f"Fuera de rango. Elige un número entre 1 y {len(available_cards)}.")
                    continue

                card = available_cards[index_card]

                if card.revealed:
                    print("Esa carta está revelada. Elige otra.")
                    continue

                if card.discarded:
                    print("Esa carta está descartada. Elige otra.")
                    continue

                return index_card

            except ValueError:
                print("Entrada inválida. Introduce un número.")

    # Hide again all Cards on the table (end of the turn)
    def hide_cards_on_table(self):
        for card in self.cards_on_table:
            card.hide()
        
