from abc import ABC

from game.Game import Game
from networking.command.Command import Command


class GameCommand(Command, ABC):
    def __init__(self, game: Game):
        self.game = game
