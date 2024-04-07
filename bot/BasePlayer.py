import random
from abc import ABC, abstractmethod
from typing import Dict, Optional

from networking.messaging.messageUtil import GAME, EVENT_TYPE, DATA


class BasePlayer(ABC):
    _valid_event_type = GAME

    def __init__(self):
        self.game_state = dict()

    @abstractmethod
    def _handle_input(self, data: dict) -> str:
        pass

    @abstractmethod
    def _handle_payment(self, data: dict) -> str:
        pass

    def handle_event(self, event: Dict) -> Optional[str]:
        if not self._valid(event):
            return
        try:
            data = event[DATA]
            data_type = data["type"]
            if data_type == "update":
                self.game_state = data
                return None
            elif data_type == "wonder_selection":
                return random.choice(data["options"])
            elif data_type == "input":
                return self._handle_input(data)
            elif data_type == "payment":
                return self._handle_payment(data)
        except KeyError:
            return

    def _valid(self, event: Dict) -> bool:
        if EVENT_TYPE in event and event[EVENT_TYPE] == self._valid_event_type:
            return True
        return False
