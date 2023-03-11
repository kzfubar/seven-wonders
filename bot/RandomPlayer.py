import random
from typing import Dict, Optional

from bot.GamePlayer import GamePlayer
from networking.messaging.messageUtil import DATA


class RandomPlayer(GamePlayer):
    def handle_event(self, event: Dict) -> Optional[str]:
        if not self._valid(event):
            return
        try:
            data = event[DATA]
            data_type = data["type"]
            if data_type == "hand":
                self.game_state["hand"] = data["hand"]
                return None
            elif data_type == "wonder_selection":
                return random.choice(data["options"])
            elif data_type == "input":
                return random.choice(data["options"]) + str(random.randrange(0, len(self.game_state["hand"])))
            elif data_type == "payment":
                return random.choice(data["options"])
        except KeyError:
            return
