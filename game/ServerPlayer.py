import queue
import threading
from _socket import SocketType
from typing import Any

from game.Player import Player
from game.Wonder import Wonder
from networking.messaging.MessageReceiver import MessageReceiver
from networking.messaging.MessageSender import MessageSender


class ServerPlayer(Player):
    def __init__(self, name: str,
                 wonder: Wonder,
                 connection: SocketType):
        self.connection = connection
        self.receiver = MessageReceiver(self.connection)
        self.sender = MessageSender(self.connection)
        self.message_queue: queue.Queue[str] = queue.Queue()
        super().__init__(name, wonder)

    def display(self, message: Any):
        self.sender.send_message(message)

    def _get_input(self, message: str) -> str:
        self.sender.send_message(message)
        msg = ''
        while msg == '':
            msg = self.message_queue.get(block=True)
        return msg

    def take_turn(self):
        threading.Thread(target=self._take_turn).start()
