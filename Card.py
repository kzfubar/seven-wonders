from typing import List


class Effect:
    def __init__(self, card_type: str):
        self.card_type = card_type

    def __repr__(self):
        return f"Effect{{}}"


class Card:
    def __init__(self, cost: List[str] = None,
                 effects: List[Effect] = None):
        self.cost = cost
        self.effects = effects

    def __repr__(self):
        return f"Card{{cost = {self.cost}, " \
               f"effects = {self.effects}}}"
