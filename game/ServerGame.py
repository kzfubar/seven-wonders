from typing import List

from server.PlayerConnection import PlayerConnection
from util.util import ALL_WONDERS
from game.Game import Game


class ServerGame(Game):
    def __init__(self, connections: List[PlayerConnection]):
        players = [x.player for x in connections]
        num_players = len(players)
        self._message_players(f"creating game with {num_players}...")

        if num_players < 3:
            raise Exception("min players is 3, t-that's fine!")  # todo make this actually message the player with error
        if num_players > len(ALL_WONDERS):
            raise Exception("more players than wonders, goober!")

        super().__init__(players)
        self.connections = connections

    def _message_players(self, message: str):
        print(message)
