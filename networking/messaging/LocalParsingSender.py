import queue

from networking.messaging.MessageSender import MessageSender


class LocalParsingSender(MessageSender):
    def __init__(self, q: queue.Queue) -> None:
        self.queue = q

    def _send(self, msg: dict) -> None:
        clean_data = msg["data"].strip("\n")
        if clean_data:
            self.queue.put(clean_data)
