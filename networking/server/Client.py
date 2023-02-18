from __future__ import annotations

import queue
import threading
from _socket import SocketType
from typing import Optional, Any

from game import ServerPlayer
from networking.messaging.MessageReceiver import MessageReceiver
from networking.messaging.MessageSender import MessageSender
from util.util import get_wonder


class Client:
    player: Optional[ServerPlayer.ServerPlayer] = None

    def __init__(self, name: str, connection: SocketType):
        self.name = name
        self.connection = connection
        self.receiver = MessageReceiver(self.connection)
        self.sender = MessageSender(self.connection)
        self.msg_queue: queue.Queue[str] = queue.Queue()

    def create_player(self, wonder_name: str) -> None:
        wonder = get_wonder(wonder_name)
        if wonder is None:
            self.sender.send_error("Wonder not found!", 1)
            return  # todo kill the connection, or ask for a different wonder name if this happens
        self.player = ServerPlayer.ServerPlayer(self.name, wonder, self)
        print(f"created {self.player}")

    def _on_message(self, callback):
        msg = ""
        while msg == "":
            msg = self.msg_queue.get(block=True)
        callback(msg)

    def on_message(self, message: str, callback) -> None:
        self.send_message(message)
        threading.Thread(target=self._on_message, args=(callback,)).start()

    def send_message(self, message: Any):
        self.sender.send_message(message)
