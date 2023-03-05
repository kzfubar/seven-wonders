from abc import ABC, abstractmethod
from typing import List

from networking.server.ClientConnection import ClientConnection


class Command(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def execute(self, args: List, client: ClientConnection):
        pass
