from typing import Dict

from bot.BasePlayer import BasePlayer


class CheapPlayer(BasePlayer):
    def _handle_input(self, data: dict) -> str:
        cards: Dict = data["options"]["play"]
        payment_option = 0
        index = 0
        payment_cost = 999  # big number to start
        own_data = self.game_state["self"]
        for card, cost in cards.items():
            min_cost = min((sum(payment) for payment in cost), default=999)
            if min_cost < payment_cost:
                for i in range(len(cost)):
                    if sum(cost[i]) < payment_option:
                        payment_option = i
                payment_cost = min_cost
                index = own_data["hand"].index(str(card))
        if payment_cost > own_data["tokens"]["coins"]:
            return "d0"
        else:
            response = "p" + str(index)
            return response

    def _handle_payment(self, data: dict) -> str:
        return "0"
