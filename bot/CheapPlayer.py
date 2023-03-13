import random
from typing import Dict, Optional

from bot.GamePlayer import GamePlayer
from networking.messaging.messageUtil import DATA


class SequentialPlayer(GamePlayer):
    def __init__(self):
        self._payment_option = 0

        super().__init__()

    def handle_event(self, event: Dict) -> Optional[str]:
        if not self._valid(event):
            return
        try:
            data = event[DATA]
            data_type = data["type"]
            if data_type == "update":
                self._payment_option = 0
                self.game_state = data
                return None
            elif data_type == "wonder_selection":
                return random.choice(data["options"])
            elif data_type == "input":
                cards: Dict = data['options']['play']
                payment_option = 0
                index = 0
                payment_cost = 999  # big number to start
                for card, cost in cards.items():
                    min_cost = min((sum(payment) for payment in cost), default=999)
                    if min_cost < payment_cost:
                        for i in range(len(cost)):
                            if sum(cost[i]) < payment_option:
                                payment_option = i
                        payment_cost = min_cost
                        index = self.game_state["hand"].index(card)
                if payment_cost > self.game_state["coins"]:
                    return "d0"
                else:
                    response = "p" + str(index)
                    self._payment_option = payment_option
                    return response
            elif data_type == "payment":
                print(self._payment_option)
                return str(self._payment_option)
        except KeyError:
            return
