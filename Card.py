from typing import List


class Effect:
    def __init__(self, effect: str,
                 resources: List[str],
                 target: List[str],
                 direction: List[str],
                 is_public: bool):
        self.effect = effect
        self.resources = resources
        self.target = target
        self.direction = direction
        self.is_public = is_public

    def __repr__(self):
        return f"Effect{{effect = {self.effect}, " \
               f"resources = {self.resources}, " \
               f"target = {self.target}, " \
               f"direction = {self.direction}, " \
               f"is_public = {self.is_public}}}"


class Card:
    def __init__(self, name: str,
                 age: int,
                 card_type: str,
                 cost: List[str],
                 effects: List[Effect]):
        self.name = name
        self.age = age
        self.card_type = card_type
        self.cost = cost
        self.effects = effects

    def __repr__(self):
        return f"Card{{name = {self.name}, " \
               f"age = {self.age}, " \
               f"card_type = {self.card_type}, " \
               f"cost = {self.cost}, " \
               f"effects = {self.effects}}}"
