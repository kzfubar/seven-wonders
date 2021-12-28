import json
import os
import pprint
import random
from typing import Optional

from game.Card import *
from game.Wonder import *

CUR_DIR = os. getcwd()


# todo eventually we'll need to refactor wonder.json to allow for multi effects
def all_wonders() -> List[Wonder]:
    with open(CUR_DIR+'/resources/wonders.json') as f:
        data = json.load(f)
        return [Wonder(wonder['name'],
                       wonder['resources'],
                       [Card(f"{wonder['name']}{i}",
                             0,
                             "wonder_power",
                             card['cost'],
                             _get_effects({"effects": [card],
                                           "type": "wonder"}))
                        for i, card in enumerate(wonder['state'])])
                for wonder in data]


def get_wonder(wonder_name: str) -> Optional[Wonder]:
    for wonder in ALL_WONDERS:
        if wonder.name.lower() == wonder_name.lower():
            return wonder
    print("Wonder not found!")
    return None


def is_resource(effect: Effect) -> bool:
    return effect.card_type == "common" or effect.card_type == "luxury"


def _get_effects(card_raw) -> List[Effect]:
    effects_raw = card_raw['effects']
    effects = []
    for effect in effects_raw:
        effects.append(Effect(effect=effect['effect'],
                              resources=effect['resources'],
                              target=effect['target'],
                              direction=effect['direction'],
                              card_type=card_raw['type']))
    return effects


def get_all_cards(num_players: int) -> List[Card]:
    with open("../resources/cards.json", 'r') as f:
        all_cards_raw = json.load(f)

    all_cards = []
    guilds = []
    for card in all_cards_raw:
        if card['type'] == 'guild':
            guilds.append(Card(name=card['name'],
                               age=card['age'],
                               card_type=card['type'],
                               cost=card['cost'],
                               effects=_get_effects(card)))
            continue

        for player_count in card['players']:
            if num_players >= player_count:
                all_cards.append(Card(name=card['name'],
                                      age=card['age'],
                                      card_type=card['type'],
                                      cost=card['cost'],
                                      effects=_get_effects(card)))
    return all_cards + random.sample(guilds, num_players + 2)


def min_cost(payment_options) -> int:
    return min(total_payment(payment) for payment in payment_options)


def total_payment(payment: Tuple[int, int]):
    return left_payment(payment) + right_payment(payment)


def left_payment(payment: Tuple[int, int]):
    return payment[0]


def right_payment(payment: Tuple[int, int]):
    return payment[1]


ALL_WONDERS = all_wonders()
LEFT = "left"
RIGHT = "right"
pprint.pprint(ALL_WONDERS)
resource_map = {
    # common
    "w": "wood",
    "s": "stone",
    "b": "brick",
    "o": "ore",

    # luxury
    "l": "loom",
    "g": "glass",
    "p": "paper",

    # token
    "v": "victory_point",
    "m": "military_might",
    "c": "coin",

    # science
    "y": "cog",
    "x": "compass",
    "z": "tablet",
}
