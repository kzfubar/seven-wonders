import queue

from networking.messaging.MessageSender import MessageSender


class LocalParsingSender(MessageSender):
    def __init__(self, q: queue.Queue):
        self.queue = q

    def _send(self, msg: dict):
        clean_data = msg["data"].strip("\n")
        if clean_data:
            self.queue.put(clean_data)
