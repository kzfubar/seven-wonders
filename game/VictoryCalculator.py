import copy
import itertools
from collections import defaultdict
from typing import Dict, List

from game.Card import Card
from game.Player import Player
from util.constants import COINS


def _to_effect_mapping(cards: List[Card]) -> Dict[int, Card]:
    effect_id_to_card = dict()
    for card in cards:
        for effect in card.effects:
            effect_id_to_card[effect.effect_id] = card
    return effect_id_to_card


class VictoryCalculator:
    def __init__(self, cards: List[Card]):
        self.effect_id_to_card: Dict[int, Card] = _to_effect_mapping(cards)

    def _to_card_name(self, effect_id) -> str:
        return (
            self.effect_id_to_card[effect_id].name
            if effect_id in self.effect_id_to_card
            else "other"
        )

    def get_victory(self, player: Player) -> Dict:
        vp = defaultdict(int)
        vp["military"] = player.military_points() - player.defeat()
        vp[COINS] = player.coins() // 3

        # calculate science
        science_counts = {"x": 0, "y": 0, "z": 0}
        science_choices = []

        for effect in player.effects["research"]:
            if len(effect.resources) > 1:
                science_choices.append(
                    tuple(resource.key for resource in effect.resources)
                )
            else:
                science_counts[effect.resources[0].key] += 1
        # covers wonder, civil, guild, and commercial cards
        for effect in player.effects["victory"]:
            if effect.target:
                for target, direction in itertools.product(
                    effect.target, effect.direction
                ):
                    effect_vp = (
                        player.neighbors[direction].token_count(target)
                        * effect.resources[0].amount
                    )
                    vp[effect.card_type] += effect_vp

            else:
                vp[effect.card_type] += effect.resources[0].amount

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

