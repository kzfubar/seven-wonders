from __future__ import annotations

from collections import defaultdict
from itertools import starmap
from typing import TYPE_CHECKING, Any

from game.Card import Card, Effect, resource_to_human
from game.Resource import Resource
from game.Tableau import Tableau
from util.constants import (
    COINS,
    DEFEAT,
    LEFT,
    MILITARY_MIGHT,
    MILITARY_POINTS,
    RIGHT,
    TRADABLE_TYPES,
)
from util.toggles import DISPLAY_TYPE, EOR_EFFECTS

if TYPE_CHECKING:
    from game.Flag import Flag
    from game.Wonder import Wonder
    from networking.server.ClientConnection import ClientConnection


class Player:
    def __init__(self, wonder: Wonder, client: ClientConnection) -> None:
        self._tableau = Tableau()

        self.client: ClientConnection = client
        self.name: str = client.name
        self.wonder: Wonder = wonder
        self.hand: list[Card] = []
        self.discards: list[Card] = []
        self.updates: list[
            str
        ] = []  # update queue to display at start of player's turn
        self.discounts: defaultdict[str, set] = defaultdict(set)
        self.next_coins: defaultdict[str, int] = defaultdict(int)
        self.coupons: set[str] = set()
        self.effects: defaultdict[str, list[Effect]] = defaultdict(list)
        self.cards_played: dict[Card, dict] = {}

        self.coins_gained: dict[str, int] = defaultdict(int)
        self.discount_coins_saved: dict[str, dict[str, int]] = {
            "luxury": {"left": 0, "right": 0},
            "common": {"left": 0, "right": 0},
        }
        self.flags: dict[Flag, bool] = {}
        self.add_token(COINS, 3)
        self.neighbors: dict[str, Player | None] = {
            LEFT: None,
            RIGHT: None,
            "self": self,
        }
        self.hand_printouts = []
        self.toggles = {DISPLAY_TYPE: True, EOR_EFFECTS: True}
        self.status: str = "is waiting around"
        self.display(f"Created player {client.name} with {wonder.name}")

    def __repr__(self) -> str:
        return (
            f"Player{{wonder = {self.wonder}, \n"
            f"tableau = {self._tableau}, \n"
            f"hand = {self.hand}, \n"
            f"effects = {self.effects}, \n"
        )

    def __str__(self) -> str:
        e: list[str] = []
        for effects in self.effects.values():
            e.extend(str(effect) for effect in effects)
        effects = "\n".join(e)
        left = self.neighbors[LEFT]
        right = self.neighbors[RIGHT]
        return (
            f"wonder = {self.wonder} \n"
            f"tableau = {self._tableau} \n"
            f"effects = {effects} \n"
            f"neighbors = {left.name if left is not None else 'NONE'} <-"
            f" {self.name} -> "
            f"{right.name if right is not None else 'NONE'} \n"
        )

    def _to_update_data(self, player: Player) -> dict:
        return {
            "cards_played": [card.id for card in player.cards_played],
            "tokens": player._tableau.tokens,
        }

    def event_update(self) -> None:
        update_data = []
        player = self.neighbors[RIGHT]
        while player != self:
            if player is None:
                return
            update_data.append(self._to_update_data(player))
            player = player.neighbors[RIGHT]
        data = {
            "type": "update",
            "self": {
                "hand": [card.id for card in self.hand],
                "cards_played": [card.id for card in self.cards_played],
                "tokens": self._tableau.tokens,
            },
            "opponents": update_data,
        }
        self.client.send_event("game", data)

    def short_info(self) -> str:
        return (
            f"{self.name} on {self.wonder.name} at level {self.wonder.level}\n"
            + f"{self._tableau.token_info()}\n"
            + f"{self._tableau.card_type_info()}\n"
            + f"{self.consolidated_effects()}"
        )

    def token_count(self, token: str) -> int:
        if token == "wonder_level":
            return self.wonder.level
        return self._tableau.count(token)

    def add_token(self, token: str, count: int) -> bool:
        return self._tableau.add(token, count)

    def add_card_type(self, card_type: str) -> bool:
        return self._tableau.add_card_type(card_type)

    def coins(self) -> int:
        return self._tableau.tokens[COINS]

    def military_might(self) -> int:
        return self._tableau.tokens[MILITARY_MIGHT]

    def military_points(self) -> int:
        return self._tableau.tokens[MILITARY_POINTS]

    def defeat(self) -> int:
        return self._tableau.tokens[DEFEAT]

    def consolidated_effects(self) -> str:
        consolidated: list[str] = []
        for e, effects in self.effects.items():
            if e == "produce":
                consolidated.extend(self._consolidated_production(effects))
            else:
                d = defaultdict(int)
                complicated = []
                for effect in effects:
                    if (
                        effect.card_type in TRADABLE_TYPES
                        and len(effect.resources) == 1
                    ):
                        resource = effect.resources[0]
                        d[resource.key] += resource.amount
                    else:
                        complicated.append(effect)
        return "\n".join(consolidated)

    def _consolidated_production(self, effects: list[Effect]) -> list[str]:
        consolidated = []
        t_simple = defaultdict(int)
        t_multi = []
        nt_simple = defaultdict(int)
        nt_multi = []
        for effect in effects:
            if len(effect.resources) == 1:
                resource = effect.resources[0]
                if effect.card_type in TRADABLE_TYPES:
                    t_simple[resource.key] += resource.amount
                else:
                    nt_simple[resource.key] += resource.amount
            elif effect.card_type in TRADABLE_TYPES:
                t_multi.append(effect)
            else:
                nt_multi.append(effect)
        tradeable = resource_to_human(list(starmap(Resource, t_simple.items())))
        tradeable.extend([str(e) for e in t_multi])
        if tradeable:
            consolidated.append(f"Tradeable Production : {', '.join(tradeable)}")
        nontradeable = resource_to_human(list(starmap(Resource, nt_simple.items())))
        nontradeable.extend([str(e) for e in nt_multi])
        if nontradeable:
            consolidated.append(f"Non-Tradeable Production: {', '.join(nontradeable)}")
        return consolidated

    def cache_printout(self, message: str) -> None:
        if message:
            self.hand_printouts.append(message)

    def clear_printouts(self) -> None:
        self.hand_printouts.clear()

    def display_printouts(self) -> None:
        for printout in self.hand_printouts:
            self.display(printout)

    def display(self, message: Any) -> None:
        self.client.send_message(message)

    async def get_input(self, msg: str) -> str:
        self.display(msg)
        return await self.client.get_message()

    def enable_flags(self) -> None:
        for flag in self.flags:
            self.flags[flag] = True

    def available_coupons(self) -> set[str]:
        return {card.name for card in self.hand}.intersection(self.coupons)

    def discard_hand(self) -> None:
        self.discards.append(*self.hand)

    def handle_next_coins(self, coins: int, direction: str) -> None:
        self.next_coins[direction] += coins

    def add_coupons(self, coupons: set[str]) -> None:
        self.coupons |= coupons

    def update_coins(self) -> None:
        for k, v in self.next_coins.items():
            self._tableau.add(COINS, v)
            if k in {LEFT, RIGHT} and v != 0:
                neighbor = self.neighbors[k]
                if neighbor is None:
                    continue
                self.updates.append(f"Received {v} coins from {neighbor.name}")
        self.next_coins = defaultdict(int)

    def get_effect_resources(self, effect: Effect) -> tuple[str, int]:
        count = 0
        for direction in effect.direction:
            player = self.neighbors[direction]
            if player is None:
                raise ValueError
            if effect.target:
                for target in effect.target:
                    count += player.token_count(target) * effect.resources[0].amount
                    # todo fix this if (multiple generate?)
            else:
                count += effect.resources[0].amount
        return effect.resources[0].key, count

    def get_neighbors(self) -> tuple[Player, Player]:
        left = self.neighbors[LEFT]
        right = self.neighbors[RIGHT]

        if left is None or right is None:
            raise Exception("player has no neighbors")
        return left, right
