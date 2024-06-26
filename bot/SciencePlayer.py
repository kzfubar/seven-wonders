from typing import Dict

from bot.BasePlayer import BasePlayer
from util.cardUtils import get_all_cards_dict
from util.constants import SCIENCE


class SciencePlayer(BasePlayer):
    def __init__(self):
        super().__init__()
        self.all_cards = get_all_cards_dict()

    def _get_lowest_cost_card_id(self, cards: dict):
        lowest_id = ""
        payment_option = 0
        payment_cost = 999  # big number to start
        for card_id, cost in cards.items():
            min_cost = min((sum(payment) for payment in cost), default=999)
            if min_cost < payment_cost:
                for i in range(len(cost)):
                    if sum(cost[i]) < payment_option:
                        payment_option = i
                payment_cost = min_cost
                lowest_id = card_id
        return lowest_id

    def _handle_input(self, data: dict) -> str:
        cards: Dict = data["options"]["play"]
        own_data = self.game_state["self"]
        science_cards = {}
        for card_id, cost in cards.items():
            card = self.all_cards[card_id]
            if card.card_type == SCIENCE:
                science_cards[card_id] = cost

        payment_cost = 999
        lowest_id = ""
        if science_cards:
            lowest_id = self._get_lowest_cost_card_id(science_cards)
            if lowest_id != "":
                payment_cost = min((sum(payment) for payment in cards[lowest_id]))

        if not science_cards or lowest_id == "" or payment_cost > 2:
            lowest_id = self._get_lowest_cost_card_id(cards)
            if lowest_id != "":
                payment_cost = min((sum(payment) for payment in cards[lowest_id]))

        if payment_cost > own_data["tokens"]["coins"]:
            return "d0"
        else:
            index = own_data["hand"].index(str(lowest_id))
            response = "p" + str(index)
            return response

    def _handle_payment(self, data: dict) -> str:
        return "0"
