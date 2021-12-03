from typing import List

from Card import Card


class Wonder:
    level = 0

    def __init__(self, name: str,
                 resource: str,
                 powers: List[Card]):
        print("wonder :0")

        self.name = name
        self.resource = resource
        self.powers = powers

    def __repr__(self):
        return f"Wonder{{name = {self.name}, " \
               f"resource = {self.resource}, " \
               f"powers = {self.powers}"

    def get_next_power(self):
        return self.powers[self.level]
