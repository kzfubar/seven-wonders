from Card import *
from Wonder import *
import json
import pprint


def all_wonders():
    with open('wonders.json') as f:
        data = json.load(f)
        return [Wonder(wonder['name'], wonder['resources'], [__get_effects({"effects": [card]}) for card in wonder['state']]) for wonder in data]



def __is_resource(card_raw):
    if 'type' in card_raw:
        return card_raw['type'] == "common" or card_raw['type'] == "luxury"
    return False

def __get_effects(card_raw):
    effects_raw = card_raw['effects']
    effects = []
    for effect in effects_raw:
        effects.append(Effect(effect=effect['effect'],
                              resources=effect['resources'],
                              target=effect['target'],
                              direction=effect['direction'],
                              is_public=__is_resource(card_raw)))
    return effects


def get_all_cards(num_players: int):
    with open("cards.json", 'r') as f:
        all_cards_raw = json.load(f)

    all_cards = []
    for card in all_cards_raw:
        for player_count in card['players']:
            if num_players >= player_count:
                all_cards.append(Card(name=card['name'],
                                      age=card['age'],
                                      card_type=card['type'],
                                      cost=card['cost'],
                                      effects=__get_effects(card)))
    return all_cards


pprint.pprint(get_all_cards(3))
all_wonders = all_wonders()
