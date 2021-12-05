from collections import Counter
from typing import Dict, Set

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
    coupons: Set[Card] = set()
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

    def take_turn(self) -> bool:
        print(f"your hand is:\n{self._hand_to_str()}")
        print(f"Bury cost: {min_cost(self._get_payment_options(self.wonder.get_next_power()))}")
        player_input = list(input("(p)lay, (d)iscard or (b)ury a card: ").replace(' ', ''))
        action = player_input[0]
        if len(player_input) > 1:
            return self._take_action(action, int(player_input[1]))
        return self._take_action(action)

    def _hand_to_str(self) -> str:
        return '\n'.join(f"({i}) {str(card)} | Cost: {min_cost(self._get_payment_options(card))}"
                         for i, card in enumerate(self.hand))

    def _menu(self) -> bool:
        print("menu")
        return False

    def _take_action(self, action: str, card_index: int = None) -> bool:
        if action == 'm':
            return self._menu()
        card = self.hand[card_index]
        if action == 'p':
            return self._play(card)
        elif action == 'd':
            return self._discard(card)
        elif action == 'b':
            return self._bury(card)
        else:
            print(f"Invalid action! {action}")
            return False

    def _play(self, card: Card) -> bool:
        print(f"playing {card}")
        # todo do any action at all
        return True

    def _discard(self, card: Card) -> bool:
        print(f"discarding {card}")
        self.board['coins'] += 3
        return True

    def _bury(self, card: Card) -> bool:
        print(f"burying {card.name}")
        wonder_power = self.wonder.get_next_power()
        successfully_played = self._play_card(wonder_power)
        if successfully_played:
            self.hand.remove(card)
        return successfully_played

    def _play_card(self, card: Card) -> bool:
        print(card)
        payment_options = self._get_payment_options(card)
        self._display_payment_options(payment_options)
        player_input = int(input("select a payment option: "))
        selected_option = payment_options[player_input]
        # todo increment neighbors coins, and decrement own coins
        # todo activate effects of card
        return True

    def _display_payment_options(self, payment_options):
        print("Payment options:")
        for i, option in enumerate(payment_options):
            print(f"({i}) {self.neighbors[LEFT].name} -> {option[0]}, {self.neighbors[RIGHT].name} -> {option[1]}")

    def _get_payment_options(self, card: Card) -> List[Tuple[int, int]]:
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
        # todo military, treasury//3, wonder state, civilian structures, commercial effects, science
        vp = 0
        vp += self.board["military_points"]
        vp += self.board["coins"] // 3
        for effects in self.effects["victory"]:
            vp += effects.resources[0][1]
        return vp
