from typing import List

from game.ServerPlayer import ServerPlayer
from util.util import ALL_WONDERS
from game.Game import Game


class ServerGame(Game):
    def __init__(self, players: List[ServerPlayer]):
        num_players = len(players)
        if num_players < 3:
            raise Exception("min players is 3, t-that's fine!")  # todo make this actually message the player with error
        if num_players > len(ALL_WONDERS):
            raise Exception("more players than wonders, goober!")

        super().__init__(players)
        self._message_players(f"creating game with {num_players}...")

    def _message_players(self, message: str):
        for player in self.players:
            player.display(message)
