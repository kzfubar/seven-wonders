from collections import Counter
from util import *

class Player:
    hand = []
    board = {
        "shame": 0,
        "military_points": 0,
        "coins": 0,
        "common": 0,
        "luxury": 0,
        "civilian": 0,
        "commercial": 0,
        "military": 0,
        "science": 0,
        "guild": 0
    }
    effects = []
    left = None
    right = None

    def __init__(self, wonder: Wonder):
        print(f"creating player {wonder}")
        self.wonder = wonder

    def __repr__(self):
        return f"Player{{wonder = {self.wonder}, " \
               f"played = {self.played}, " \
               f"hand = {self.hand}, " \
               f"coins = {self.coins}, " \
               f"shame = {self.shame}, " \
               f"military_points = {self.military_points}}}"

    def hand_to_str(self):
        hand = ""
        for card in self.hand:
            hand += f"{card.name}{{{card.card_type}}}, {card.effects}\n"
        return hand

    def get_min_cost(self, card: Card, effects: List[Effect]):
        resources = [effect for effect in effects if is_resource(effect)]

        for resource, count in Counter(card.cost).items():
            pass


