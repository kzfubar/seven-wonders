from abc import ABC, abstractmethod

from networking.server.ClientConnection import ClientConnection


class Command(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def execute(self, args: list[str], client: ClientConnection) -> None:
        pass
