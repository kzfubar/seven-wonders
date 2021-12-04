import json
import pprint
import random

from Card import *
from Wonder import *


def all_wonders() -> List[Wonder]:
    with open('wonders.json') as f:
        data = json.load(f)
        return [Wonder(wonder['name'],
                       wonder['resources'],
                       [Card(f"{wonder['name']}{i}",
                             0,
                             "wonder_power",
                             card['cost'],
                             __get_effects({"effects": [card]}))
                        for i, card in enumerate(wonder['state'])])
                for wonder in data]


def __is_resource(card_raw) -> bool:
    if 'type' in card_raw:
        return card_raw['type'] == "common" or card_raw['type'] == "luxury"
    return False


def __get_effects(card_raw) -> List[Effect]:
    effects_raw = card_raw['effects']
    effects = []
    for effect in effects_raw:
        effects.append(Effect(effect=effect['effect'],
                              resources=effect['resources'],
                              target=effect['target'],
                              direction=effect['direction'],
                              is_public=__is_resource(card_raw)))
    return effects


def get_all_cards(num_players: int) -> List[Card]:
    with open("cards.json", 'r') as f:
        all_cards_raw = json.load(f)

    all_cards = []
    guilds = []
    for card in all_cards_raw:
        if card['type'] == 'guild':
            guilds.append(Card(name=card['name'],
                               age=card['age'],
                               card_type=card['type'],
                               cost=card['cost'],
                               effects=__get_effects(card)))
            continue

        for player_count in card['players']:
            if num_players >= player_count:
                all_cards.append(Card(name=card['name'],
                                      age=card['age'],
                                      card_type=card['type'],
                                      cost=card['cost'],
                                      effects=__get_effects(card)))
    return all_cards + random.sample(guilds, num_players + 2)


def min_cost(payment_options) -> int:
    return min(a + b for a, b in payment_options)


ALL_WONDERS = all_wonders()
LEFT = "left"
RIGHT = "right"
pprint.pprint(ALL_WONDERS)
