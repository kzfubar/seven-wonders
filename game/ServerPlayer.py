from __future__ import annotations
import threading
from typing import Any

from game.Player import Player
from game.Wonder import Wonder
from networking.server.Client import Client


class ServerPlayer(Player):
    def __init__(self, name: str, wonder: Wonder, client: Client):
        self.client = client
        super().__init__(name, wonder)

    def display(self, message: Any):
        self.client.send_message(message)

    def _on_input(self, message: str, callback) -> None:
        self.client.on_message(message, callback)
