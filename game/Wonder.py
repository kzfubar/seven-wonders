from typing import List

from game.Card import Card
from game.Side import Side
from util.utils import cards_as_string


class Wonder:
    def __init__(
        self, name: str, base_name: str, side: Side, power: Card, stages: List[Card]
    ):
        self.name: str = name
        self.base_name: str = base_name
        self.side: Side = side
        self.power = power
        self.stages = stages
        self.level = 0
        self.is_max_level = False

    def __repr__(self):
        return (
            f"Wonder{{name = {self.name}, "
            f"power = {self.power}, "
            f"stages = {self.stages}, "
            f"level = {self.level}"
        )

    def __str__(self):
        header, stages_str = cards_as_string(self.stages, False)
        stages = (
            "    "
            + header
            + "\n"
            + "\n".join(
                f"({'x' if self.level > i else ' '}) {stages_str[stage]}"
                for i, stage in enumerate(self.stages)
            )
        )
        return f"{self.name} \n" f"power = {self.power} \n" f"{stages} "

    def get_next_stage(self) -> Card:
        return self.stages[self.level]

    def increment_level(self):
        self.level += 1
        if self.level >= len(self.stages):
            self.is_max_level = True
