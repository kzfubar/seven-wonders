import random
from typing import Dict, Optional

from bot.GamePlayer import GamePlayer
from networking.messaging.messageUtil import DATA


class SequentialPlayer(GamePlayer):
    def __init__(self):
        self._cur_index = 0

        super().__init__()

    def handle_event(self, event: Dict) -> Optional[str]:
        if not self._valid(event):
            return
        try:
            data = event[DATA]
            data_type = data["type"]
            if data_type == "hand":
                self._cur_index = 0
                self.game_state["hand"] = data["hand"]
                return None
            elif data_type == "wonder_selection":
                return random.choice(data["options"])
            elif data_type == "input":
                if self._cur_index == len(self.game_state["hand"]):
                    return "d0"
                else:
                    response = "p" + str(self._cur_index)
                    self._cur_index += 1
                    return response
            elif data_type == "payment":
                return random.choice(data["options"])
        except KeyError:
            return
