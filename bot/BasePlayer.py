import random
from abc import ABC, abstractmethod

from networking.messaging.messageUtil import DATA, EVENT_TYPE, GAME


class BasePlayer(ABC):
    _valid_event_type = GAME

    def __init__(self) -> None:
        self.game_state = {}

    @abstractmethod
    def _handle_input(self, data: dict) -> str:
        pass

    @abstractmethod
    def _handle_payment(self, data: dict) -> str:
        pass

    def handle_event(self, event: dict) -> str | None:
        if not self._valid(event):
            return None
        try:
            data = event[DATA]
            data_type = data["type"]
            if data_type == "update":
                self.game_state = data
                return None
            if data_type == "wonder_selection":
                return random.choice(data["options"])
            if data_type == "input":
                return self._handle_input(data)
            if data_type == "payment":
                return self._handle_payment(data)
        except KeyError:
            return None

    def _valid(self, event: dict) -> bool:
        return bool(EVENT_TYPE in event and event[EVENT_TYPE] == self._valid_event_type)
