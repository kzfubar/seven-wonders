from abc import ABC, abstractmethod
from typing import Optional


class MessageReceiver(ABC):
    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    async def get_message(self) -> Optional[dict]:
        pass


class EmptyReceiver(MessageReceiver):
    def is_empty(self):
        pass

    async def get_message(self) -> Optional[dict]:
        pass


EMPTY_RECEIVER = EmptyReceiver()
