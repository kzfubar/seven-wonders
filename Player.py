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
    coupons = set()
    effects = []
    neighbors = {
        LEFT: None,
        RIGHT: None
    }

    def __init__(self, wonder: Wonder):
        print(f"creating player {wonder}")
        self.wonder = wonder

    def __repr__(self):
        return f"Player{{wonder = {self.wonder}, " \
               f"board = {self.board}, " \
               f"hand = {self.hand}, "

    def hand_to_str(self):
        return '\n'.join(f"({i}) {str(card)} | Cost: {min_cost(self.get_payment_options(card))}"
                         for i, card in enumerate(self.hand))

    def take_action(self, action: str, card_index: int):
        if action == 'p':
            self.__play(card_index)
        elif action == 'd':
            self.__discard(card_index)
        elif action == 'b':
            self.__bury(card_index)
        else:
            raise Exception("we currently don't handle invalid actions!")  # todo

    def __play(self, card_index: int):
        card = self.hand.pop(card_index)
        print(f"playing {card}")
        # todo do any action at all

    def __discard(self, card_index: int):
        card = self.hand.pop(card_index)
        print(f"discarding {card}")
        self.board['coins'] += 3

    def __bury(self, card_index: int):
        card = self.hand.pop(card_index)
        print(f"burying {card}")
        # todo do any action at all


    def get_payment_options(self, card: Card) -> List[Tuple[int]]: 
        return [(1, 0)]


        for resource, count in Counter(card.cost).items():
            pass
