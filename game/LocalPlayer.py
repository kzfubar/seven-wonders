from typing import Any

from game.Player import Player


class LocalPlayer(Player):
    turn_over = True

    def display(self, message: Any):
        print(message)

    def _get_input(self, message) -> str:
        return input(message)

    def take_turn(self):
        self._take_turn()


