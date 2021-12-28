from util import *
from Player import Player
from game.Game import Game


class LocalGame(Game):
    def __init__(self, num_players):
        print(f"creating game with {num_players}...")

        if num_players < 3:
            raise Exception("min players is 3, t-that's fine!")
        if num_players > len(ALL_WONDERS):
            raise Exception("more players than wonders, goober!")

        players = [Player(str(i), wonder) for i, wonder in enumerate(random.sample(ALL_WONDERS, num_players))]

        super().__init__(players)

    def _message_players(self, message: str):
        print(message)
