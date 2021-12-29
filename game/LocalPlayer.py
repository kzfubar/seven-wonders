from typing import Any

from game.Player import Player


class LocalPlayer(Player):
    def display(self, message: Any):
        print(message)

