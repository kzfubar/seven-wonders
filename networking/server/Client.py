from __future__ import annotations
import asyncio

import queue
from _socket import SocketType
from typing import Any
import threading

from networking.messaging.MessageReceiver import MessageReceiver
from networking.messaging.MessageSender import MessageSender


class Client:
    def __init__(self, name: str, connection: SocketType):
        self.name = name
        self.connection = connection
        self.receiver = MessageReceiver(self.connection)
        self.sender = MessageSender(self.connection)
        self.msg_queue: queue.Queue[str] = queue.Queue()

    async def get_message(self):
        while not self.msg_queue.not_empty:
            await asyncio.sleep(500)

        return self.msg_queue.get()

    def send_message(self, message: Any):
        self.sender.send_message(message)

    def _on_message(self, callback):
        msg = ""
        while msg == "":
            msg = self.msg_queue.get(block=True)
        callback(msg)

    def on_message(self, message: str, callback) -> None:
        self.send_message(message)
        threading.Thread(target=self._on_message, args=(callback,)).start()
