from typing import List

from game.Card import Card
from util.constants import RESOURCE_MAP
from util.utils import cards_as_string


class Wonder:
    def __init__(self, name: str, resource: str, powers: List[Card]):
        self.name = name
        self.resource = resource
        self.powers = powers
        self.level = 0
        self.is_max_level = False

    def __repr__(self):
        return (
            f"Wonder{{name = {self.name}, "
            f"resource = {self.resource}, "
            f"powers = {self.powers}, "
            f"level = {self.level}"
        )

    def __str__(self):
        header, powers_str = cards_as_string(self.powers, False)
        powers = "    " + header + "\n" + "\n".join(
            f"({'x' if self.level > i else ' '}) {powers_str[power]}"
            for i, power in enumerate(self.powers)
        )
        return (
            f"{self.name} \n"
            f"resource = {RESOURCE_MAP[self.resource]} \n"
            f"{powers} "
        )

    def get_next_power(self) -> Card:
        return self.powers[self.level]

    def increment_level(self):
        self.level += 1
        if self.level >= len(self.powers):
            self.is_max_level = True
