from collections import defaultdict
from typing import DefaultDict
from typing import Dict, Set, Any, List, Optional, Tuple

from game.Card import Card, Effect, resource_to_human
from game.Flag import Flag
from game.Resource import Resource
from game.Tableau import Tableau
from game.Wonder import Wonder
from networking.server.ClientConnection import ClientConnection
from util.constants import (
    LEFT,
    RIGHT,
    COINS,
    TRADABLE_TYPES,
    DEFEAT,
    MILITARY_POINTS,
    MILITARY_MIGHT,
)
from util.toggles import DISPLAY_TYPE, EOR_EFFECTS


class Player:
    def __init__(self, wonder: Wonder, client: ClientConnection):
        self._tableau = Tableau()

        self.client: ClientConnection = client
        self.name: str = client.name
        self.wonder: Wonder = wonder
        self.hand: List[Card] = []
        self.discards: List[Card] = []
        self.updates: List[
            str
        ] = []  # update queue to display at start of player's turn
        self.discounts: DefaultDict[str, set] = defaultdict(set)
        self.next_coins: DefaultDict[str, int] = defaultdict(int)
        self.coupons: Set[str] = set()
        self.effects: DefaultDict[str, List[Effect]] = defaultdict(list)
        self.cards_played: Dict[Card, Dict] = dict()

        self.coins_gained: Dict[str, int] = defaultdict(int)
        self.discount_coins_saved: Dict[str, Dict[str, int]] = {"luxury": {"left": 0, "right": 0},
                                                                "common": {"left": 0, "right": 0}
                                                                }
        self.flags: Dict[Flag, bool] = dict()
        self.add_token(COINS, 3)
        self.neighbors: Dict[str, Optional[Player]] = {
            LEFT: None,
            RIGHT: None,
            "self": self,
        }
        self.hand_printouts = []
        self.toggles = {DISPLAY_TYPE: True, EOR_EFFECTS: True}
        self.status: str = "is waiting around"
        self.display(f"Created player {client.name} with {wonder.name}")

    def __repr__(self):
        return (
            f"Player{{wonder = {self.wonder}, \n"
            f"tableau = {self._tableau}, \n"
            f"hand = {self.hand}, \n"
            f"effects = {self.effects}, \n"
        )

    def __str__(self):
        e = []
        for _, effects in self.effects.items():
            for effect in effects:
                e.append(str(effect))
        effects = "\n".join(e)
        return (
            f"wonder = {self.wonder} \n"
            f"tableau = {self._tableau} \n"
            f"effects = {effects} \n"
            f"neighbors = {self.neighbors[LEFT].name if self.neighbors[LEFT] is not None else 'NONE'} <-"
            f" {self.name} -> "
            f"{self.neighbors[RIGHT].name if self.neighbors[RIGHT] is not None else 'NONE'} \n"
        )

    def event_update(self):
        hand = {
            "type": "update",
            "hand": [card.id for card in self.hand],
            "coins": self._tableau.tokens[COINS]
        }
        self.client.send_event("game", hand)

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
        consolidated = []
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

    def _consolidated_production(self, effects: List[Effect]) -> List[str]:
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
            else:
                if effect.card_type in TRADABLE_TYPES:
                    t_multi.append(effect)
                else:
                    nt_multi.append(effect)
        tradeable = resource_to_human([Resource(key, amount) for key, amount in t_simple.items()])
        tradeable.extend([str(e) for e in t_multi])
        if tradeable:
            consolidated.append(f'Tradeable Production : {", ".join(tradeable)}')
        nontradeable = resource_to_human([Resource(key, amount) for key, amount in nt_simple.items()])
        nontradeable.extend([str(e) for e in nt_multi])
        if nontradeable:
            consolidated.append(f'Non-Tradeable Production: {", ".join(nontradeable)}')
        return consolidated

    def cache_printout(self, message: str):
        if message:
            self.hand_printouts.append(message)

    def clear_printouts(self):
        self.hand_printouts.clear()

    def display_printouts(self):
        for printout in self.hand_printouts:
            self.display(printout)

    def display(self, message: Any):
        self.client.send_message(message)

    async def get_input(self, msg: str) -> str:
        self.display(msg)
        return await self.client.get_message()

    def enable_flags(self):
        for flag in self.flags:
            self.flags[flag] = True

    def available_coupons(self) -> Set[str]:
        return set(card.name for card in self.hand).intersection(self.coupons)

    def discard_hand(self) -> None:
        self.discards.append(*self.hand)

    def handle_next_coins(self, coins: int, direction: str):
        self.next_coins[direction] += coins

    def add_coupons(self, coupons: Set[str]):
        self.coupons |= coupons

    def update_coins(self):
        for k, v in self.next_coins.items():
            self._tableau.add(COINS, v)
            if k in (LEFT, RIGHT) and v != 0:
                self.updates.append(f"Received {v} coins from {self.neighbors[k].name}")
        self.next_coins = defaultdict(int)

    def get_effect_resources(self, effect: Effect) -> Tuple[str, int]:
        count = 0
        for direction in effect.direction:
            player = self.neighbors[direction]
            if effect.target:
                for target in effect.target:
                    count += player.token_count(target) * effect.resources[0].amount
                    # todo fix this if (multiple generate?)
            else:
                count += effect.resources[0].amount
        return effect.resources[0].key, count
