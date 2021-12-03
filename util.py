from Card import *
from Wonder import *


def all_wonders():
    return [Wonder("wonder", "resource", [Card(), Card(), Card()]) for _ in range(3)]


def all_cards(age: int):
    return [Card() for _ in range(21)]


def is_resource(effect: Effect):
    return effect.card_type == "common" or effect.card_type == "luxury"


all_wonders = all_wonders()
