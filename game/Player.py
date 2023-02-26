import copy
import itertools
from collections import defaultdict
from typing import DefaultDict
from typing import Dict, Set, Any, List, Optional, Tuple

from game.Card import Card, Effect
from game.Flag import Flag
from game.Wonder import Wonder
from networking.server.ClientConnection import ClientConnection
from util.constants import (
    LEFT,
    RIGHT,
    LUXURY_GOODS, COINS,
)


class Player:
    def __init__(self, wonder: Wonder, client: ClientConnection):
        self.client = client
        self.name: str = client.name
        self.wonder: Wonder = wonder
        self.hand: List[Card] = []
        self.discards: List[Card] = []
        self.updates: List[str] = []  # update queue to display at start of player's turn
        self.discounts: DefaultDict[str, set] = defaultdict(set)
        self.next_coins: DefaultDict[str, int] = defaultdict(int)
        self.coupons: Set[str] = set()
        self.effects: DefaultDict[str, List[Effect]] = defaultdict(list)
        self.flags: Dict[Flag, bool] = dict()
        self.board: DefaultDict[str, int] = defaultdict(int)
        self.board[COINS] = 3
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

    def __str__(self):  # todo make this nicer!!
        e = []
        for _, effects in self.effects.items():
            for effect in effects:
                e.append(str(effect))
        effects = '\n'.join(e)
        return (
            f"wonder = {self.wonder} \n"
            f"board = {dict(self.board)} \n"
            f"effects = {effects}, \n"
            f"neighbors = {self.neighbors[LEFT].name if self.neighbors[LEFT] is not None else 'NONE'} <-"
            f" {self.name} -> "
            f"{self.neighbors[RIGHT].name if self.neighbors[RIGHT] is not None else 'NONE'} \n"
        )

    def display(self, message: Any):
        self.client.send_message(message)

    async def get_input(self) -> str:
        self.client.clear_message_buffer()
        return await self.client.get_message()

    def enable_flags(self):
        for flag in self.flags:
            self.flags[flag] = True

    def available_coupons(self) -> Set[str]:
        return set(card.name for card in self.hand).intersection(self.coupons)

    def discard_hand(self) -> None:
        self.discards.append(*self.hand)

    def handle_next_coins(self, coins: int, direction):
        self.next_coins[direction] += coins

    def add_coupons(self, coupons: Set[str]):
        self.coupons |= coupons

    def update_coins(self):
        for k, v in self.next_coins.items():
            self.board[COINS] += v
            if k in (LEFT, RIGHT) and v != 0:
                self.updates.append(f"Received {v} coins from {self.neighbors[k].name}")
        self.next_coins = defaultdict(int)

    def get_effect_resources(self, effect: Effect) -> Tuple[str, int]:
        count = 0
        for direction in effect.direction:
            player = self.neighbors[direction]
            if effect.target:
                for target in effect.target:
                    count += player.board[target] * effect.resources[0][1]
                    # todo fix this if (multiple generate?)
            else:
                count += effect.resources[0][1]
        return effect.resources[0][0], count

    def get_victory(self):
        vp = defaultdict(int)
        vp["military"] = self.board["military_points"] - self.board["shame"]
        vp[COINS] = self.board[COINS] // 3

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

            min_count = min(0, *curr_counts.values())
            vp["science"] = max(
                vp["science"],
                min_count * 7
                + sum(count * count for count in curr_counts.values()),
            )

        return vp
