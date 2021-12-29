from _socket import SocketType
from typing import Any

from game.Player import Player
from game.Wonder import Wonder
from messaging.MessageSender import MessageSender


class ServerPlayer(Player):
    def __init__(self, name: str,
                 wonder: Wonder,
                 connection: SocketType):
        self.connection = connection
        self.sender = MessageSender(self.connection)
        super().__init__(name, wonder)

    def display(self, message: Any):
        self.sender.send_message(message)


