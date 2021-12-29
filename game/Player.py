from collections import Counter, defaultdict
from typing import Dict, Set, DefaultDict
import math

from util.util import *


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
        "guild": 0,
        "wonder_power": 0
    }
    next_coins: int = 0
    coupons: Set[Card] = set()
    effects: DefaultDict[str, List[Effect]] = defaultdict(list)
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

    def __str__(self):  # todo make this nicer
        return f"Player{{wonder = {self.wonder}, " \
               f"board = {self.board}, " \
               f"effects = {self.effects}, "

    def take_turn(self) -> bool:
        print(f"your hand is:\n{self._hand_to_str()}")
        print(f"Bury cost: {min_cost(self._get_payment_options(self.wonder.get_next_power()))}")
        player_input = list(input("(p)lay, (d)iscard or (b)ury a card: ").replace(' ', ''))
        action = player_input[0]
        if len(player_input) > 1:
            return self._take_action(action, int(player_input[1]))
        return self._take_action(action)

    def handle_next_coins(self, coins: int):
        self.next_coins += coins

    def _hand_to_str(self) -> str:
        return '\n'.join(f"({i}) {str(card)} | Cost: {min_cost(self._get_payment_options(card))}"
                         for i, card in enumerate(self.hand))

    def _menu(self) -> bool:
        menu_options = [
            "Display player information"
        ]
        print('\n'.join(f"({i}) {str(option)}" for i, option in enumerate(menu_options)))
        selected_option = int(input("select menu option: "))
        if selected_option == 0:
            print(str(self))
        return False

    def _take_action(self, action: str, card_index: int = None) -> bool:
        if action == 'm':
            return self._menu()
        if card_index is None:
            card_index = int(input("please select a card: "))
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
        successfully_played = self._play_card(card)
        if successfully_played:
            self.hand.remove(card)
        return successfully_played

    def _discard(self, card: Card) -> bool:
        print(f"discarding {card}")
        self.board['coins'] += 3
        self.hand.remove(card)
        return True

    def _bury(self, card: Card) -> bool:
        print(f"burying {card.name}")
        wonder_power = self.wonder.get_next_power()
        successfully_played = self._play_card(wonder_power)
        if successfully_played:
            self.wonder.increment_level()
            self.hand.remove(card)
        return successfully_played

    def _play_card(self, card: Card) -> bool:
        print(card)
        payment_options = self._get_payment_options(card)
        self._display_payment_options(payment_options)
        player_input = input("select a payment option: ")
        if player_input == 'q':
            return False
        player_input = int(player_input)
        self._do_payment(payment_options[player_input])
        self._activate_card(card)
        self.board[card.card_type] += 1
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
            if effect.effect == "generate":
                resource_key, count = self._get_effect_resources(effect)
                resource = resource_map[resource_key]
                self.board[resource] += count
            else:
                self.effects[effect.effect].append(effect)

    def _do_payment(self, payment: Tuple[int, int]):
        self.neighbors[LEFT].handle_next_coins(left_payment(payment))
        self.neighbors[RIGHT].handle_next_coins(right_payment(payment))
        self.handle_next_coins(-1 * total_payment(payment))  # -1 for decrement own coins

    def _get_effect_resources(self, effect: Effect) -> Tuple[str, int]:
        count = 0
        for direction in effect.direction:
            player = self if direction == "self" else self.neighbors[direction]
            if effect.target:
                for target in effect.target:
                    count += player.board[target] * effect.resources[0][1]
            else:
                count += effect.resources[0][1]
        return effect.resources[0][0], count

    def get_victory(self):
        # todo science
        vp = 0
        vp += self.board["military_points"]
        vp += self.board["coins"] // 3
        
        # covers wonder, civil, and commercial cards
        for effects in self.effects["victory"]:
            if effects.target:
                for direction in effects.direction:
                    if direction == "left":
                        for targets in effects.target:
                            vp += self.neighbors[LEFT].board[targets] * effects.resources[0][1]
                            
                    if direction == "right":
                        for targets in effects.target:
                            vp += self.neighbors[RIGHT].board[targets] * effects.resources[0][1]
                            
                    else:
                        for targets in effects.target:
                            vp += self.board[targets] * effects.resources[0][1]
            
            else:
                vp += effects.resources[0][1]
        
        # calculate science -- doesn't take cards with choice of mat into account
        cog, compass, tablet = 0
        for effects in self.effects["research"]:
            if effects.resources[0][0] == "x":
                compass += 1
            elif effects.resources[0][0] == "y":
                cog += 1
            elif effects.resources[0][0] == "z":
                tablet += 1
        
        # Calculates set and identical cards
        vp += min(cog, compass, tablet) * 7
        vp += math.pow(cog,2) + math.pow(compass, 2) + math.pow(tablet, 2)



        return vp
