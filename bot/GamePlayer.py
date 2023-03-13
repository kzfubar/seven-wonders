from abc import ABC, abstractmethod
from typing import Dict, Optional

from networking.messaging.messageUtil import GAME, EVENT_TYPE


class GamePlayer(ABC):
    _valid_event_type = GAME

    def __init__(self):
        self.game_state = dict()

    @abstractmethod
    def handle_event(self, event: Dict) -> Optional[str]:
        pass

    def _valid(self, event: Dict) -> bool:
        if EVENT_TYPE in event and event[EVENT_TYPE] == self._valid_event_type:
            return True
        return False
