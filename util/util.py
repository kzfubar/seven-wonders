from __future__ import annotations

import json
import pprint
import random
from typing import Optional, Tuple
import itertools

from game.Card import Effect
from game.Wonder import *


# todo eventually we'll need to refactor wonder.json to allow for multi effects
def all_wonders() -> List[Wonder]:
    with open('resources/wonders.json') as f:
        data = json.load(f)
        return [Wonder(wonder['name'],
                       wonder['resources'][0],
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
    with open("./resources/cards.json", 'r') as f:
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


def min_cost(payment_options: List[Tuple[int, int, int]]) -> str:
    if len(payment_options) == 0:
        return '-' 
    return str(min(total_payment(payment) for payment in payment_options))


def total_payment(payment: Tuple[int, int, int]):
    return sum(payment)


def left_payment(payment: Tuple[int, int, int]):
    return payment[0]


def right_payment(payment: Tuple[int, int, int]):
    return payment[1]


def simplify_cost_search(effects, reqs, goods):
    choices = []

    for effect in effects:
        if len(effect.resources) != 1:
            if effect.resources[0][0] in goods:
                choices.append(tuple(resource[0] for resource in effect.resources))

        else:
            for _ in range(effect.resources[0][1]):
                if effect.resources[0][0] not in reqs: break

                reqs.remove(effect.resources[0][0])

    return choices

def find_resource_outcomes(left_effects, right_effects, choices, reqs, goods):
    outcomes = set()
    for options in itertools.product([''], *choices):
            
        reqs_curr = reqs[:]

        for option in options[1:]:
            if option in reqs_curr:
                reqs_curr.remove(option)

        for i in range(1 << len(reqs_curr)):
            left_reqs = []
            right_reqs = []
            
            for j, val in enumerate(reqs_curr):
                if i & (1 << j) == 0:
                    left_reqs.append(val)
                else:
                    right_reqs.append(val)

            l_count, r_count = len(left_reqs), len(right_reqs)
            if (l_count, r_count) in outcomes: continue

            if not valid_resources(simplify_cost_search(left_effects, left_reqs, goods), left_reqs):
                break

            if not valid_resources(simplify_cost_search(right_effects, right_reqs, goods), right_reqs):
                break

            outcomes.add((l_count, r_count))
    return outcomes


def valid_resources(choices, reqs):
    for options in itertools.product([''], *choices):
            
        reqs_curr = reqs[:]

        for option in options[1:]:
            if option in reqs_curr:
                reqs_curr.remove(option)

        if len(reqs_curr) == 0:
            return True

    return False        


TRADABLE_TYPES = set(('common', 'luxury'))
COMMON_GOODS = set('lgp')
LUXURY_GOODS = set('wsbo')

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
