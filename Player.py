from collections import Counter

from util import *


class Player:
    hand = []
    board = {
        "shame": 0,
        "military_points": 0,
        "coins": 3,
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
               f"board = {self.board}, " \
               f"hand = {self.hand}, "

    def hand_to_str(self):
        hand = ""
        for i, card in enumerate(self.hand):
            hand += f"({i}) {str(card)}\n"
        return hand

    def get_card(self, card_index):
        return self.hand[card_index]

    def get_min_cost(self, card: Card, effects: List[Effect]):
        resources = [effect for effect in effects if is_resource(effect)]

        for resource, count in Counter(card.cost).items():
            pass
