import queue
from typing import Optional, Dict


class LocalReceiver:
    def __init__(self, q: queue.Queue[Dict]):
        self.queue: queue.Queue[Dict] = q

    def is_empty(self):
        return self.queue.empty()

    async def get_message(self) -> Optional[dict]:
        return self.queue.get()
