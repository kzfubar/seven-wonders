from abc import ABC

from game.Game import Game
from networking.server.command.Command import Command


class GameCommand(Command, ABC):
    def __init__(self, game: Game) -> None:
        self.game = game
