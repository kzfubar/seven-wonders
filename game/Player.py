import copy
import itertools
from collections import defaultdict
from typing import DefaultDict
from typing import Dict, Set, Any, List, Optional, Tuple

from game.Card import Card, Effect
from game.FlagHolder import FlagHolder
from game.Wonder import Wonder
from networking.server.ClientConnection import ClientConnection
from util.constants import (
    LEFT,
    RIGHT,
    LUXURY_GOODS,
)


class Player:
    hand: List[Card] = []
    board: DefaultDict[str, int] = defaultdict(int)
    updates: List[str] = []  # update queue to display at start of player's turn
    discounts: DefaultDict[str, set] = defaultdict(set)
    next_coins: DefaultDict[str, int] = defaultdict(int)
    coupons: Set[Card] = set()
    effects: DefaultDict[str, List[Effect]] = defaultdict(list)
    flags: List[FlagHolder] = []

    client: ClientConnection
    name: str
    wonder: Wonder
    neighbors: Dict

    def __init__(self, wonder: Wonder, client: ClientConnection):
        self.client = client
        self.name: str = client.name
        self.wonder: Wonder = wonder
        self.board["coins"] = 3
        self.neighbors: Dict[str, Optional[Player]] = {
            LEFT: None,
            RIGHT: None,
            "self": self,
        }
        self.effects["produce"].append(
            Effect(
                effect="produce",
                resources=[(wonder.resource, 1)],
                target=[],
                direction=["self"],
                card_type="luxury" if wonder.resource in LUXURY_GOODS else "common",
            )
        )

        self.display(f"Created player {client.name} with {wonder.name}")

    def __repr__(self):
        return (
            f"Player{{wonder = {self.wonder}, \n"
            f"board = {self.board}, \n"
            f"hand = {self.hand}, \n"
            f"effects = {self.effects}, \n"
        )

    def __str__(self):  # todo make this nicer
        return (
            f"wonder = {self.wonder} \n"
            f"board = {self.board} \n"
            f"effects = {self.effects}, \n"
            f"neighbors = {self.neighbors[LEFT].name if self.neighbors[LEFT] is not None else 'NONE'} <-"
            f" {self.name} -> "
            f"{self.neighbors[RIGHT].name if self.neighbors[RIGHT] is not None else 'NONE'} \n"
        )

    def display(self, message: Any):
        self.client.send_message(message)

    def handle_next_coins(self, coins: int, direction):
        self.next_coins[direction] += coins

    def update_coins(self):
        for k, v in self.next_coins.items():
            self.board["coins"] += v
            if k in (LEFT, RIGHT) and v != 0:
                self.updates.append(f"Received {v} coins from {self.neighbors[k].name}")
        self.next_coins = defaultdict(int)

    def get_effect_resources(self, effect: Effect) -> Tuple[str, int]:
        count = 0
        for direction in effect.direction:
            player = self if direction == "self" else self.neighbors[direction]
            if effect.target:
                for target in effect.target:
                    count += player.board[target] * effect.resources[0][1]
            else:
                count += effect.resources[0][1]
        return effect.resources[0][0], count

    def get_victory(self):
        vp = defaultdict(int)
        vp["military"] = self.board["military_points"] - self.board["shame"]
        vp["coins"] = self.board["coins"] // 3

        # covers wonder, civil, guild, and commercial cards
        for effect in self.effects["victory"]:
            if effect.target:
                for target, direction in itertools.product(
                        effect.target, effect.direction
                ):
                    vp[effect.card_type] += (
                            self.neighbors[direction].board[target] * effect.resources[0][1]
                    )

            else:
                vp[effect.card_type] += effect.resources[0][1]

        # calculate science
        science_counts = defaultdict(int)
        science_choices = []

        for effect in self.effects["research"]:
            if len(effect.resources) > 1:
                science_choices.append(
                    tuple(resource[0] for resource in effect.resources)
                )

            science_counts[effect.resources[0][0]] += 1

        for options in itertools.product([""], *science_choices):
            curr_counts = copy.copy(science_counts)

            for option in options[1:]:
                curr_counts[option] += 1

            vp["science"] = max(
                vp["science"],
                min(curr_counts.values()) * 7
                + sum(count * count for count in curr_counts.values()),
            )

        return vp
