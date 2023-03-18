import json
import random
from typing import List, Dict, Tuple

from game.Card import Card, Effect
from game.Resource import Resource


def get_effects(card_raw: Dict, effect_id: int) -> Tuple[List[Effect], int]:
    effects_raw = card_raw["effects"]
    effects = []
    for effect in effects_raw:
        effects.append(
            Effect(
                effect=effect["effect"],
                resources=[Resource(r[0], r[1]) for r in effect["resources"]],
                target=effect["target"],
                direction=effect["direction"],
                card_type=card_raw["type"],
                effect_id=effect_id
            ))
        effect_id += 1
    return effects, effect_id


def get_all_cards(num_players: int) -> List[Card]:
    with open("./resources/cards.json", "r") as f:
        all_cards_raw = json.load(f)

    all_cards = []
    guilds = []
    effect_id = 0
    for raw_card in all_cards_raw:
        if raw_card["type"] == "guild":
            effects, effect_id = get_effects(raw_card, effect_id)
            guilds.append(Card(
                id=raw_card["id"],
                name=raw_card["name"],
                age=raw_card["age"],
                card_type=raw_card["type"],
                cost=raw_card["cost"],
                coupons=raw_card["coupon"],
                effects=effects))
            continue

        for player_count in raw_card["players"]:
            if num_players >= player_count:
                effects, effect_id = get_effects(raw_card, effect_id)
                all_cards.append(
                    Card(
                        id=raw_card["id"],
                        name=raw_card["name"],
                        age=raw_card["age"],
                        card_type=raw_card["type"],
                        cost=raw_card["cost"],
                        coupons=raw_card["coupon"],
                        effects=effects,
                    )
                )
    return all_cards + random.sample(guilds, num_players + 2)
