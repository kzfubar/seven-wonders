import json
import random
from typing import List, Dict

from game.Card import Card, Effect
from game.Resource import Resource
from util.constants import MAX_PLAYERS


def to_card_id(name: str, suffix: str = "") -> str:
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
                effect_id=f"{card_id}_{i}",
            )
        )
    return effects


def get_all_cards_dict() -> Dict[str, Card]:
    all_cards = get_all_cards(MAX_PLAYERS)
    all_cards_dict = {card.id: card for card in all_cards}
    return all_cards_dict


def get_all_cards(num_players: int) -> List[Card]:
    with open("./resources/cards.json", "r") as f:
        all_cards_raw = json.load(f)

    cards_by_name: Dict[str, Card] = {}
    coupons_by_card: Dict[str, List[str]] = {}
    all_cards = []
    guilds = []
    for raw_card in all_cards_raw:
        if raw_card["type"] == "guild":
            card_name = raw_card["name"]
            card_id = to_card_id(card_name)
            effects = get_effects(raw_card, card_id)
            guilds.append(
                Card(
                    card_id=card_id,
                    name=card_name,
                    age=raw_card["age"],
                    card_type=raw_card["type"],
                    cost=raw_card["cost"],
                    effects=effects,
                )
            )
            continue

        for player_count in raw_card["players"]:
            if num_players >= player_count:
                card_id = to_card_id(raw_card["name"], str(player_count))
                effects = get_effects(raw_card, card_id)
                card = Card(
                    card_id=card_id,
                    name=raw_card["name"],
                    age=raw_card["age"],
                    card_type=raw_card["type"],
                    cost=raw_card["cost"],
                    effects=effects,
                )
                all_cards.append(card)
                coupons_by_card[raw_card["name"]] = raw_card["coupon"]
                cards_by_name[raw_card["name"]] = card

    for card in all_cards:
        coupons = [cards_by_name[coupon] for coupon in coupons_by_card[card.name]]
        card.set_coupons(coupons)

    return all_cards + random.sample(guilds, num_players + 2)
