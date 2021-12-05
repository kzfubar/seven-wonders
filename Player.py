from collections import Counter
from typing import Dict

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
    effects: Dict[str, List[Effect]] = {}
    neighbors: Dict[str, 'Player'] = {
        LEFT: None,
        RIGHT: None
    }

    def __init__(self, name: str, wonder: Wonder):
        print(f"creating player {name} with {wonder.name}")
        self.name = name
        self.wonder = wonder

    def __repr__(self):
        return f"Player{{wonder = {self.wonder}, " \
               f"board = {self.board}, " \
               f"hand = {self.hand}, "

    def hand_to_str(self) -> str:
        return '\n'.join(f"({i}) {str(card)} | Cost: {min_cost(self.get_payment_options(card))}"
                         for i, card in enumerate(self.hand))

    def take_action(self, action: str, card_index: int):
        card = self.hand.pop(card_index)
        if action == 'p':
            self._play(card)
        elif action == 'd':
            self._discard(card)
        elif action == 'b':
            self._bury(card)
        else:
            raise Exception("we currently don't handle invalid actions!")  # todo

    def _play(self, card: Card):
        print(f"playing {card}")
        # todo do any action at all

    def _discard(self, card: Card):
        print(f"discarding {card}")
        self.board['coins'] += 3

    def _bury(self, card: Card):
        print(f"burying {card.name}")
        wonder_power = self.wonder.get_next_power()
        self._activate_card(wonder_power)

    def _activate_card(self, card: Card):
        print(card)
        payment_options = self.get_payment_options(card)
        self._display_payment_options(payment_options)
        player_input = int(input("select a payment option: "))
        selected_option = payment_options[player_input]
        # todo increment neighbors coins, and decrement own coins
        # todo activate effects of card

    def _display_payment_options(self, payment_options):
        print("Payment options:")
        for i, option in enumerate(payment_options):
            print(f"({i}) {self.neighbors[LEFT].name} -> {option[0]}, {self.neighbors[RIGHT].name} -> {option[1]}")

    def get_payment_options(self, card: Card) -> List[Tuple[int, int]]:
        return [(1, 0)]

        for resource, count in Counter(card.cost).items():
            pass

    def _activate_card(self, card: Card):
        for effect in card.effects:
            self._handle_effect(effect)
            if effect not in self.effects:
                self.effects[effect.effect] = []
            self.effects[effect.effect].append(effect)

    def _handle_effect(self, effect: Effect):
        if effect.effect == "generate":
            pass  # todo

    def get_victory(self):
        # military, treasury//3, wonder state, civilian structures, commercial effects, science
        vp = 0
        vp += self.board["military_points"]
        vp += self.board["coins"] // 3
        
        for effects in self.effects["victory"]:
            vp += effects.resources[0][1]
        
    
        return vp

        





    