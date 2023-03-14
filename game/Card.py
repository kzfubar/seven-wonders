from collections import defaultdict
from typing import ItemsView, List, Tuple, DefaultDict, Union

from game.Resource import Resource
from util.ANSI import ANSI, use
from util.constants import RESOURCE_MAP, TYPE_COLOR_MAP


class Effect:
    def __init__(
        self,
        effect: str,
        resources: List[Resource],
        target: List[str],
        direction: List[str],
        card_type: str,
        effect_id: int = 0,
    ):
        self.effect_id = effect_id
        self.effect = effect
        self.resources = resources
        self.target = target
        self.direction = direction
        self.card_type = card_type

    def __repr__(self):
        return (
            f"Effect{{effect = {self.effect}, "
            f"resources = {self.resources}, "
            f"target = {self.target}, "
            f"direction = {self.direction}, "
            f"card_type = {self.card_type}}}"
        )

    def __str__(self):
        s = f"{self.effect}"
        targets = []
        if self.target:
            for target in self.target:
                color = (
                    TYPE_COLOR_MAP[target]
                    if target in TYPE_COLOR_MAP
                    else ANSI.BRIGHT_WHITE
                )
                targets.append(use(color, target))
        if self.resources:
            resources = " or ".join(resource_to_human(self.resources))
            s += f" {resources}"
        s += f" for {', '.join(self.direction)}" if self.direction != ["self"] else ""
        s += f" on {', '.join(targets)}" if targets else ""
        return s


class Card:
    def __init__(
        self,
        id: int,
        name: str,
        age: int,
        card_type: str,
        cost: List[str],
        coupons: List[str],
        effects: List[Effect],
    ):
        self.id = id
        self.name = name
        self.age = age
        self.card_type = card_type
        self.cost = cost
        self.coupons = coupons
        self.effects = effects

    def __repr__(self):
        return (
            f"Card{{name = {self.name}, "
            f"age = {self.age}, "
            f"card_type = {self.card_type}, "
            f"cost = {self.cost}, "
            f"coupon = {self.coupons}, "
            f"effects = {self.effects}}}"
        )

    def __str__(self):
        color = (
            TYPE_COLOR_MAP[self.card_type]
            if self.card_type in TYPE_COLOR_MAP
            else ANSI.BRIGHT_WHITE
        )
        return f"{use(color, self.name)} - {self.effects_to_str()}"

    def effects_to_str(self) -> str:
        effects = [str(e) for e in self.effects]
        return " & ".join(effects)

    def resource_to_str(self) -> str:
        resource_dict: DefaultDict[str, int] = defaultdict(int)
        for resource in self.cost:
            resource_dict[resource] += 1
        resources = [Resource(key, amount) for key, amount in resource_dict.items()]
        resources_str = ", ".join(resource_to_human(resources))
        return "-" if resources_str == "" else resources_str


def resource_to_human(
    resources: List[Resource]
) -> List[str]:
    return [
        f"{resource.amount} {RESOURCE_MAP[resource.key]}" for resource in resources
    ]
