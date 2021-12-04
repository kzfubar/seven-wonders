from typing import List

from Card import Card


class Wonder:
    def __init__(self, name: str,
                 resource: str,
                 powers: List[Card]):
        self.name = name
        self.resource = resource
        self.powers = powers
        self.level = 0

    def __repr__(self):
        return f"Wonder{{name = {self.name}, " \
               f"resource = {self.resource}, " \
               f"powers = {self.powers}, " \
               f"level = {self.level}"

    def get_next_power(self) -> Card:
        return self.powers[self.level]
