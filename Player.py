from Card import *
from Wonder import Wonder
from collections import Counter
from util import *

class Player:
    hand = [Card]
    played = [Card]
    effects = [Effect]
    coins = 0
    shame = 0
    military_points = 0
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

    def get_min_cost(self, card: Card, effects: List[Effect]):
        resources = [effect for effect in effects if is_resource(effect)]

        for resource, count in Counter(card.cost).items():
            pass


