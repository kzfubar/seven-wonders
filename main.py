from game.LocalGame import LocalGame


def main():
    num_players = int(input("num players: "))
    game = LocalGame(num_players)
    game.play()


if __name__ == "__main__":
    print("it's time to play seven wonders!")
    main()
