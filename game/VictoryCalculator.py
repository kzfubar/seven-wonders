import copy
import itertools
from collections import defaultdict
from typing import Dict, List

from game.Card import Card
from game.Player import Player
from util.constants import COINS, MILITARY_MIGHT


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
        return self.effect_id_to_card[effect_id].name if effect_id in self.effect_id_to_card else "other"

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

    def get_vp_per_card(self, player: Player) -> Dict:
        card_vp = defaultdict(int)
        vp = defaultdict(int, self.get_victory(player))
        # deduct coin cost from card value, and distribute defeat across non military cards
        for effect in player.effects["generate"]:
            card_name = self._to_card_name(effect.effect_id)
            resource = effect.resources[0].key
            if resource == "c":
                if effect.target:
                    for target, direction in itertools.product(
                            effect.target, effect.direction
                    ):
                        resource_count = (
                                player.neighbors[direction].token_count(target) * effect.resources[0].amount
                        )
                        card_vp[card_name] += resource_count / 3

                else:
                    card_vp[card_name] += effect.resources[0].amount / 3
            if resource == "m":
                # not possible to have military points without might
                military_percent = effect.resources[0].amount / player._tableau.tokens[MILITARY_MIGHT]
                card_vp[card_name] += player.military_points() * military_percent

        for card, play_data in player.cards_played.items():
            card_vp[card.name] -= play_data["cost"] / 3
            if card.card_type != "military":
                card_vp[card.name] -= player.defeat() / len(player.cards_played)

        for effect in player.effects["discount"]:
            card_name = self._to_card_name(effect.effect_id)
            for resource_type, saved_by_direction in player.discount_coins_saved.items():
                for direction, coins_saved in saved_by_direction.items():
                    points = coins_saved / 3
                    if resource_type in effect.target and direction in effect.direction:
                        card_vp[card_name] += points

        for resource, coins_gained in player.coins_gained.items():
            card_names = []
            points = coins_gained / 3
            for effect in player.effects["produce"]:
                if resource in [r.key for r in effect.resources]:
                    name = self._to_card_name(effect.effect_id)
                    card_names.append(name)
            for card_name in card_names:
                card_vp[card_name] += points / len(card_names)

        # covers wonder, civil, guild, and commercial cards
        for effect in player.effects["victory"]:
            card_name = self._to_card_name(effect.effect_id)
            if effect.target:
                for target, direction in itertools.product(
                        effect.target, effect.direction
                ):
                    effect_vp = (
                            player.neighbors[direction].token_count(target)
                            * effect.resources[0].amount
                    )
                    vp[effect.card_type] += effect_vp
                    card_vp[card_name] += effect_vp

            else:
                vp[effect.card_type] += effect.resources[0].amount
                card_vp[card_name] += effect.resources[0].amount

        for effect in player.effects["research"]:
            card_name = self._to_card_name(effect.effect_id)
            card_vp[card_name] += vp["science"] / len(player.effects["research"])

        return dict(card_vp)
