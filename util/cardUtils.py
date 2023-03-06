import json
import random
from typing import List, Dict

from game.Card import Card, Effect


def get_effects(card_raw: Dict) -> List[Effect]:
    effects_raw = card_raw["effects"]
    effects = []
    for effect in effects_raw:
        effects.append(
            Effect(
                effect=effect["effect"],
                resources=effect["resources"],
                target=effect["target"],
                direction=effect["direction"],
                card_type=card_raw["type"],
            )
        )
    return effects


def get_all_cards(num_players: int) -> List[Card]:
    with open("./resources/cards.json", "r") as f:
        all_cards_raw = json.load(f)

    all_cards = []
    guilds = []
    for card in all_cards_raw:
        if card["type"] == "guild":
            guilds.append(
                Card(
                    name=card["name"],
                    age=card["age"],
                    card_type=card["type"],
                    cost=card["cost"],
                    coupons=card["coupon"],
                    effects=get_effects(card),
                )
            )
            continue

        for player_count in card["players"]:
            if num_players >= player_count:
                all_cards.append(
                    Card(
                        name=card["name"],
                        age=card["age"],
                        card_type=card["type"],
                        cost=card["cost"],
                        coupons=card["coupon"],
                        effects=get_effects(card),
                    )
                )
    return all_cards + random.sample(guilds, num_players + 2)
