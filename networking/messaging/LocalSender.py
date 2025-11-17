import queue

from networking.messaging.MessageSender import MessageSender


class LocalSender(MessageSender):
    def __init__(self, q: queue.Queue) -> None:
        self.queue = q

    def _send(self, msg: dict) -> None:
        self.queue.put(msg)
