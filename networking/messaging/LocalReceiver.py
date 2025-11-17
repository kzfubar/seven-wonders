import queue

from networking.messaging.MessageReceiver import MessageReceiver


class LocalReceiver(MessageReceiver):
    def __init__(self, q: queue.Queue) -> None:
        self.queue = q

    def is_empty(self) -> bool:
        return self.queue.empty()

    async def get_message(self) -> dict:
        return self.queue.get()
