import queue

from networking.messaging.MessageSender import MessageSender


class LocalSender(MessageSender):
    def __init__(self, q: queue.Queue):
        self.queue = q

    def _send(self, msg: dict):
        self.queue.put(msg)
