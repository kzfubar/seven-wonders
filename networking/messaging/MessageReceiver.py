from abc import ABC, abstractmethod


class MessageReceiver(ABC):
    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    async def get_message(self) -> dict:
        pass


class EmptyReceiver(MessageReceiver):
    def is_empty(self) -> bool:
        return True

    async def get_message(self) -> dict:
        return {}


EMPTY_RECEIVER = EmptyReceiver()
