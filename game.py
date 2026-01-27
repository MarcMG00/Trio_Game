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
        print("Cartas :")
        current_player.display_own_cards()

        # Continue turn until 2-3 Cards are not the same
        while True:
            print("------------Start------------")
            # Show other player's Cards
            self.display()

            print("\nElige una acción :")
            print("1 - Girar una carta del centro")
            print("2 - Pedir una carta a otro jugador")
            print("3 - Girar una carta propia")

            choice = input("Opción: ")

            if choice == "1":
                self.flip_card_on_table()
            elif choice == "2":
                self.ask_card_another_player(current_player)
            elif choice == "3":
                self.flip_own_card(current_player)
            else:
                print("Opción inválida.")

            # Show other player's Cards (to show new Card revealed if a player was asked)
            self.display()

            # Check if current Cards revealed allows to player to get a Trio
            self.apply_trio(current_player)

            # Turn ends if current player hasn't got same numbers when choosing OR if has scored
            if not self.can_still_be_trio or current_player.has_scored_current_turn:
                self.hide_cards_on_table()
                self.hide_players_cards()
                self.numbers_revealed_on_current_turn = []
                break

        print("------------End------------")
        # Hide current player Cards
        current_player.hide_own_cards()
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
    
    # Option 2 - Ask a Card to another player
    def ask_card_another_player(self, current_player):
        print(f"Elige un jugador a quien pedir una carta :")
        
        player_to_ask = self.get_player(current_player)

        print(f"1 - Carta menos alta | 2 - Carta más alta : ")
        option = int(input("Opción : "))

        # Reveal Card from player chosen
        self.reveal_card_other_player(player_to_ask, option, False)

        return
    
    # Option 3 - Flip own Card
    def flip_own_card(self, current_player):
        print(f"1 - Carta menos alta | 2 - Carta más alta : ")
        option = int(input("Opción : "))

        # Reveal Card from current player
        self.reveal_card_other_player(current_player, option, True)

        return

    # Get player to ask a Card
    def get_player(self, current_player):
        # Show players available
        for p in self.players:
            if p != current_player:
                print(f"Jugador {p.number}")

        while True:
            try:
                player_number = int(input("Jugador : "))

                # Search for player with this number
                target_player = next((p for p in self.players if p.number == player_number), None)

                if target_player is None:
                    print("Jugador inexistente.")
                    continue

                if target_player == current_player:
                    print("No puedes elegirte a ti mismo.")
                    continue

                return target_player

            except ValueError:
                print("Entrada inválida. Introduce un número.")

    # Reveal a card from player chosen
    def reveal_card_other_player(self, player_to_ask, option, is_current_player):
        card_revealed = player_to_ask.reveal_card(option, is_current_player)
        # Put value from card revealed on list to compare
        self.numbers_revealed_on_current_turn.append(card_revealed.value)

    # Get if current player can still ask for Cards (and do a trio)
    def can_still_be_trio(self) -> bool:
        nums = self.numbers_revealed_on_current_turn

        if len(nums) <= 1:
            return True

        return len(set(nums)) == 1
    
    # Check if got a trio
    def apply_trio(self, player):
        trio_num = self.trio_number()

        if trio_num is None:
            return

        player.nb_trios += 1
        player.has_scored_current_turn = True

        # Condition to get the victory
        if player.nb_trios == 3 or trio_num == 7:
            player.is_winner = True

    # Get the number from the trio
    def trio_number(self) -> int | None:
        if self.is_trio():
            return self.numbers_revealed_on_current_turn[0]
        return None
    
    # Get if is a trio
    def is_trio(self) -> bool:
        nums = self.numbers_revealed_on_current_turn
        return len(nums) == 3 and len(set(nums)) == 1

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

    # Hide other player's cards (end of the turn)
    def hide_players_cards(self):
        current_player = self.players[self.current_player_index]
        for player in self.players:
            if player is current_player:
                continue
            player.hide_own_cards()

    # Show player's Cards (but no current player playing the turn)
    def display(self):
        current_player = self.players[self.current_player_index]
        for player in self.players:
            if player is current_player:
                continue
            player.display()
        
