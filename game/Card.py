from collections import defaultdict
from typing import List, Tuple, DefaultDict

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
            resources = ' or '.join(util.resource_to_human(self.resources))
            s += f" {resources}"
        s += f" for {', '.join(self.direction)}" if self.direction != ['self'] else ''
        s += f" on {', '.join(self.target)}" if self.target else ''
        return s


class Card:
    def __init__(self, name: str,
                 age: int,
                 card_type: str,
                 cost: List[str],
                 coupons: List[str],
                 effects: List[Effect]):
        self.name = name
        self.age = age
        self.card_type = card_type
        self.cost = cost
        self.coupons = coupons
        self.effects = effects

    def __repr__(self):
        return f"Card{{name = {self.name}, " \
               f"age = {self.age}, " \
               f"card_type = {self.card_type}, " \
               f"cost = {self.cost}, " \
               f"cost = {self.coupons}, " \
               f"effects = {self.effects}}}"

    def __str__(self):
        return f"{self.name} | {self.card_type} | {self.effects_to_str()} | {self.resource_to_str()}"

    def effects_to_str(self) -> str:
        effects = [str(e) for e in self.effects]
        return ' & '.join(effects)

    def resource_to_str(self) -> str:
        resources: DefaultDict[str, int] = defaultdict(int)
        for resource in self.cost:
            resources[resource] += 1
        resources_str = ', '.join(util.resource_to_human(resources.items()))
        return f"Resource: {resources_str}"
