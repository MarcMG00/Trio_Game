from game import Game

# to start a Console Game => command : "python main.py"
# Only can play between 3 to 6 players
def ask_number_of_players(min_players=3, max_players=6):
    while True:
        try:
            num = int(input("Número de jugadores: "))
            if min_players <= num <= max_players:
                return num
            else:
                print(f"El número debe estar entre {min_players} y {max_players}.")
        except ValueError:
            print("Solo se puede jugar de 3 a 6 jugadores.")

# Start game
def main():
    nb_players = ask_number_of_players()
    game = Game(nb_players)
    game.setup()

    # Starts game
    game.play()

# Init game
if __name__ == "__main__":
    main()