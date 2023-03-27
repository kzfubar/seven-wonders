from collections import defaultdict
from typing import List, DefaultDict
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
        effect_id: str,
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


def _to_id(name: str) -> str:
    return name.replace(" ", "").lower()


class Card:
    def __init__(
        self,
        card_id: str,
        name: str,
        age: int,
        card_type: str,
        cost: List[str],
        effects: List[Effect],
    ):
        self._color = (
            TYPE_COLOR_MAP[card_type]
            if card_type in TYPE_COLOR_MAP
            else ANSI.BRIGHT_WHITE
        )
        self.name: str = name
        self.age: int = age
        self.card_type: str = card_type
        self.cost: List[str] = cost
        self.effects: List[Effect] = effects
        self.id: str = card_id
        self.coupons: List['Card'] = []

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
        return f"{self.with_color(self.name)} - {self.effects_to_str()}"

    def with_color(self, s: str) -> str:
        return use(self._color, s)

    def set_coupons(self, coupons: List['Card']):
        self.coupons = coupons

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
