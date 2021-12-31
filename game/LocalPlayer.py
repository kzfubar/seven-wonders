from typing import Any

from game.Player import Player


class LocalPlayer(Player):
    turn_over = True

    def display(self, message: Any):
        print(message)

    def _on_input(self, message: str, callback) -> None:
        player_input = input(message)
        callback(player_input)
