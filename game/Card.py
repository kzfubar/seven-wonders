from typing import List, Tuple

from util import util


class Effect:
    def __init__(self, effect: str,
                 resources: List[Tuple[str, int]],
                 target: List[str],
                 direction: List[str],
                 card_type: str):
        self.effect = effect
        self.resources = resources
        self.target = target
        self.direction = direction
        self.card_type = card_type

    def __repr__(self):
        return f"Effect{{effect = {self.effect}, " \
               f"resources = {self.resources}, " \
               f"target = {self.target}, " \
               f"direction = {self.direction}, " \
               f"card_type = {self.card_type}}}"

    def __str__(self):
        s = f"{self.effect}"
        if self.resources:
            resources = ' or '.join([f"{amount} {util.resource_map[resource_key]}" for resource_key, amount in self.resources])
            s += f" {resources}"
        s += f" for {', '.join(self.direction)}" if self.direction != ['self'] else ''
        s += f" on {', '.join(self.target)}" if self.target else ''
        return s


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

    def __str__(self):
        effects = [str(e) for e in self.effects]
        return f"{self.name:17} | {self.card_type:10} | {' & '.join(effects):30} | Resource: {''.join(self.cost)}"
