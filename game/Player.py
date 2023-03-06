import copy
import itertools
from collections import defaultdict
from typing import DefaultDict
from typing import Dict, Set, Any, List, Optional, Tuple

from game.Card import Card, Effect, resource_to_human
from game.Flag import Flag
from game.Tableau import Tableau
from game.Wonder import Wonder
from networking.server.ClientConnection import ClientConnection
from util.constants import LEFT, RIGHT, COINS, WONDER, TRADABLE_TYPES, DEFEAT, MILITARY_POINTS, MILITARY_MIGHT


class Player:
    def __init__(self, wonder: Wonder, client: ClientConnection):
        self._tableau = Tableau()

        self.client = client
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
        self.flags: Dict[Flag, bool] = dict()
        self.add_token(COINS, 3)
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
                card_type=WONDER,
            )
        )

        self.display(f"Created player {client.name} with {wonder.name}")

    def __repr__(self):
        return (
            f"Player{{wonder = {self.wonder}, \n"
            f"tableau = {self._tableau}, \n"
            f"hand = {self.hand}, \n"
            f"effects = {self.effects}, \n"
        )

    def __str__(self):  # todo make this nicer!!
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

    def short_info(self) -> str:
        return f"{self.name} on {self.wonder.name} at level {self.wonder.level}\n" \
               + f"\t{self._tableau.token_info()}\n" \
               + f"\t{self._tableau.card_type_info()}\n" \
               + f"\t{self.consolidated_effects()}"

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
                    if effect.card_type in TRADABLE_TYPES and len(effect.resources) == 1:
                        resources = effect.resources[0]
                        d[resources[0]] += resources[1]
                    else:
                        complicated.append(effect)
        return '\n'.join(consolidated)

    def _consolidated_production(self, effects: List[Effect]) -> List[str]:
        consolidated = []
        t_simple = defaultdict(int)
        t_multi = []
        nt_simple = defaultdict(int)
        nt_multi = []
        for effect in effects:
            if len(effect.resources) == 1:
                resources = effect.resources[0]
                if effect.card_type in TRADABLE_TYPES:
                    t_simple[resources[0]] += resources[1]
                else:
                    nt_simple[resources[0]] += resources[1]
            else:
                if effect.card_type in TRADABLE_TYPES:
                    t_multi.append(effect)
                else:
                    nt_multi.append(effect)
        tradeable = resource_to_human(t_simple.items())
        tradeable.extend([str(e) for e in t_multi])
        if tradeable:
            consolidated.append(f'Tradeable Production : {", ".join(tradeable)}')
        nontradeable = resource_to_human(nt_simple.items())
        nontradeable.extend([str(e) for e in nt_multi])
        if nontradeable:
            consolidated.append(f'Non-Tradeable Production: {", ".join(nontradeable)}')
        return consolidated

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
                    count += player.token_count(target) * effect.resources[0][1]
                    # todo fix this if (multiple generate?)
            else:
                count += effect.resources[0][1]
        return effect.resources[0][0], count

    def get_victory(self) -> Dict:
        vp = defaultdict(int)
        vp["military"] = self.military_points() - self.defeat()
        vp[COINS] = self.coins() // 3

        # covers wonder, civil, guild, and commercial cards
        for effect in self.effects["victory"]:
            if effect.target:
                for target, direction in itertools.product(
                        effect.target, effect.direction
                ):
                    vp[effect.card_type] += (
                            self.neighbors[direction].token_count(target) * effect.resources[0][1]
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

            min_count = min(curr_counts.values(), default=0)
            vp["science"] = max(
                vp["science"],
                min_count * 7 + sum(count * count for count in curr_counts.values()),
            )

        return dict(vp)
