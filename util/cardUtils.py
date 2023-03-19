import json
import random
from typing import List, Dict

from game.Card import Card, Effect
from game.Resource import Resource


def to_card_id(name: str, suffix='') -> str:
    return name.replace(" ", "").lower() + suffix


def get_effects(card_raw: Dict, card_id: str) -> List[Effect]:
    effects_raw = card_raw["effects"]
    effects = []
    for i, effect in enumerate(effects_raw):
        effects.append(
            Effect(
                effect=effect["effect"],
                resources=[Resource(r[0], r[1]) for r in effect["resources"]],
                target=effect["target"],
                direction=effect["direction"],
                card_type=card_raw["type"],
                effect_id=f"{card_id}_{i}"
            ))
    return effects


def get_all_cards(num_players: int) -> List[Card]:
    with open("./resources/cards.json", "r") as f:
        all_cards_raw = json.load(f)

    all_cards = []
    guilds = []
    for raw_card in all_cards_raw:
        if raw_card["type"] == "guild":
            card_name = raw_card["name"]
            card_id = to_card_id(card_name)
            effects = get_effects(raw_card, card_id)
            guilds.append(Card(
                card_id=card_id,
                name=card_name,
                age=raw_card["age"],
                card_type=raw_card["type"],
                cost=raw_card["cost"],
                coupons=raw_card["coupon"],
                effects=effects))
            card_name.append(card_name)
            continue

        for player_count in raw_card["players"]:
            if num_players >= player_count:
                card_id = to_card_id(raw_card["name"], player_count)
                effects = get_effects(raw_card, card_id)
                all_cards.append(
                    Card(
                        card_id=card_id,
                        name=raw_card["name"],
                        age=raw_card["age"],
                        card_type=raw_card["type"],
                        cost=raw_card["cost"],
                        coupons=raw_card["coupon"],
                        effects=effects,
                    )
                )
    return all_cards + random.sample(guilds, num_players + 2)
