from typing import Optional

from networking.messaging.MessageReceiver import MessageReceiver


class LocalReceiver(MessageReceiver):
    def __init__(self, q):
        self.queue = q

    def is_empty(self):
        return self.queue.empty()

    async def get_message(self) -> Optional[dict]:
        return self.queue.get()
