from __future__ import annotations

import asyncio
import queue
from typing import Any, Dict

from networking.messaging.MessageSender import MessageSender


class ClientConnection:
    def __init__(self, name: str, sender: MessageSender):
        self.name = name
        self.sender = sender
        self.msg_queue: queue.Queue[str] = queue.Queue()

    def __repr__(self):
        return f"{self.name}"

    def clear_message_buffer(self,):
        while not self.msg_queue.empty():
            self.msg_queue.get()

    async def get_message(self) -> str:
        while self.msg_queue.empty():
            await asyncio.sleep(1)
        return self.msg_queue.get()

    def send_message(self, message: Any):
        self.sender.send_message(message)

    def send_event(self, event_type: str, data: Dict):
        self.sender.send_event(event_type, data)

    def _on_message(self, callback):
        msg = ""
        while msg == "":
            msg = self.msg_queue.get(block=True)
        callback(msg)
