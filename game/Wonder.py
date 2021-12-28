from typing import List

from game.Card import Card


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

    def __str__(self):  # todo make this look nice
        powers = '\n'.join(str(power) for power in self.powers)
        return f"Wonder{{name = {self.name}, " \
               f"resource = {self.resource}, " \
               f"powers = \n{powers}\n " \
               f"level = {self.level}"

    def get_next_power(self) -> Card:  # todo we should check to make sure we can't bury if level exceeded
        return self.powers[self.level]  # todo this will throw an exception at max level

    def increment_level(self):  # todo we can check if this is incremented too much
        self.level += 1

