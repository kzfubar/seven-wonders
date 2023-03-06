from collections import defaultdict
from typing import ItemsView, List, Tuple, DefaultDict, Union

from util import ANSI
from util.constants import RESOURCE_MAP, TYPE_COLOR_MAP


class Effect:
    def __init__(
        self,
        effect: str,
        resources: List[Tuple[str, int]],
        target: List[str],
        direction: List[str],
        card_type: str,
    ):
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
                color = TYPE_COLOR_MAP[target] if target in TYPE_COLOR_MAP else ANSI.ANSI.WHITE
                targets.append(ANSI.use(color, target))
        if self.resources:
            resources = " or ".join(resource_to_human(self.resources))
            s += f" {resources}"
        s += f" for {', '.join(self.direction)}" if self.direction != ["self"] else ""
        s += f" on {', '.join(targets)}" if targets else ""
        return s


class Card:
    def __init__(
        self,
        name: str,
        age: int,
        card_type: str,
        cost: List[str],
        coupons: List[str],
        effects: List[Effect],
    ):
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
        return f"{self.name} | {self.card_type} | {self.effects_to_str()} | {self.resource_to_str()}"

    def effects_to_str(self) -> str:
        effects = [str(e) for e in self.effects]
        return " & ".join(effects)

    def resource_to_str(self) -> str:
        resources: DefaultDict[str, int] = defaultdict(int)
        for resource in self.cost:
            resources[resource] += 1
        resources_str = ", ".join(resource_to_human(resources.items()))
        return "-" if resources_str == "" else resources_str


def resource_to_human(
    resources: Union[ItemsView[str, int], List[Tuple[str, int]]]
) -> List[str]:
    return [
        f"{count} {RESOURCE_MAP[resource_key]}" for resource_key, count in resources
    ]
