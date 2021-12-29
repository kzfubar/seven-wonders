from collections import Counter, defaultdict
from typing import Dict, Set, DefaultDict
from abc import abstractmethod
from collections import Counter
from typing import Dict, Set, Any
import math

from util.util import *


class Player:
    def __init__(self, name: str, wonder: Wonder):
        self.display(f"creating player {name} with {wonder.name}")
        self.name = name
        self.wonder = wonder
        self.hand = []
        self.board: DefaultDict[str, int] = defaultdict(int)
        self.board['coins'] = 3

        # attr:
        #     "shame": 0,
        #     "military_points": 0,
        #     "coins": 3,
        #     "common": 0,
        #     "luxury": 0,
        #     "civilian": 0,
        #     "commercial": 0,
        #     "military": 0,
        #     "science": 0,
        #     "guild": 0,
        #     "wonder_power": 0
        
        self.next_coins: int = 0
        self.coupons: Set[Card] = set()
        self.effects: DefaultDict[str, List[Effect]] = defaultdict(list)
        self.neighbors: Dict[str, 'Player'] = {
            LEFT: None,
            RIGHT: None
        }

        self.effects['produce'].append(Effect('produce', [wonder.resource, 1], [], ['self'], 'luxury' if wonder.resource in 'lgp' else 'common'))

        self.hand_payment_options: List[List[Tuple[int, int, int]]]
        self.wonder_payment_options: List[Tuple[int, int, int]]

    def __repr__(self):
        return f"Player{{wonder = {self.wonder}, \n" \
               f"board = {self.board}, \n" \
               f"hand = {self.hand}, \n" \
               f"effects = {self.effects}, \n"

    def __str__(self):  # todo make this nicer
        return f"Player{{wonder = {self.wonder}, " \
               f"board = {self.board}, " \
               f"effects = {self.effects}, "

    @abstractmethod
    def display(self, message: Any):
        pass

    def take_turn(self) -> bool:
        self._calc_hand_costs()
        self.display(f"your hand is:\n{self._hand_to_str()}")
        self.display(f"Bury cost: {min_cost(self._get_payment_options(self.wonder.get_next_power()))}")
        player_input = list(input("(p)lay, (d)iscard or (b)ury a card: ").strip())
        action = player_input[0]
        if len(player_input) > 1:
            return self._take_action(action, int(player_input[1]))
        return self._take_action(action)

    def _calc_hand_costs(self) -> None:
        self.wonder_payment_options = self._get_payment_options(self.wonder.get_next_power())
        self.hand_payment_options = [self._get_payment_options(card) for card in self.hand]

    def handle_next_coins(self, coins: int):
        self.next_coins += coins

    def _hand_to_str(self) -> str:
        return '\n'.join(f"({i}) {str(self.hand[i]):80} Cost: {min_cost(payment_options)}"
                         for i, payment_options in enumerate(self.hand_payment_options))

    def _menu(self) -> bool:
        menu_options = [
            "Display player information"
        ]
        self.display('\n'.join(f"({i}) {str(option)}" for i, option in enumerate(menu_options)))
        selected_option = int(input("select menu option: "))
        if selected_option == 0:
            self.display(str(self))
        return False

    def _take_action(self, action: str, card_index: int = None) -> bool:
        if action == 'm':
            return self._menu()
        if card_index is None:
            card_index = int(input("please select a card: "))
        card = self.hand[card_index]
        if action == 'p':
            return self._play(card, self.hand_payment_options[card_index])
        elif action == 'd':
            return self._discard(card)
        elif action == 'b':
            return self._bury(card)
        else:
            self.display(f"Invalid action! {action}")
            return False

    def _play(self, card: Card, payment_options: List[Tuple[int, int, int]]) -> bool:
        self.display(f"playing {card}")
        successfully_played = self._play_card(card, payment_options)
        if successfully_played:
            self.hand.remove(card)
        return successfully_played

    def _discard(self, card: Card) -> bool:
        self.display(f"discarding {card}")
        self.board['coins'] += 3
        self.hand.remove(card)
        return True

    def _bury(self, card: Card) -> bool:
        self.display(f"burying {card.name}")
        wonder_power = self.wonder.get_next_power()
        successfully_played = self._play_card(wonder_power, self.wonder_payment_options)
        if successfully_played:
            self.wonder.increment_level()
            self.hand.remove(card)
        return successfully_played

    def _play_card(self, card: Card, payment_options: List[Tuple[int, int, int]]) -> bool:
        self.display(card)
        if len(payment_options) == 0:
            return False
        if payment_options[0][2] != 0:
            # cost is coins to bank
            self.handle_next_coins(-payment_options[0][2])
            return True

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
        self.display("Payment options:")
        for i, option in enumerate(payment_options):
            self.display(f"({i}) {self.neighbors[LEFT].name} -> {option[0]}, {self.neighbors[RIGHT].name} -> {option[1]}")

    def _get_payment_options(self, card: Card) -> List[Tuple[int, int, int]]:
        if 'c' in card.cost:
            return [(0, 0, card.cost.count('c'))]
        return [(1, 1, 0)]
        
        luxury_choices = []
        common_choices = []

        luxury_reqs = [good for good in card.cost if good in LUXURY_GOODS]
        common_reqs = [good for good in card.cost if good in COMMON_GOODS]

        for effect in self.effects:
            if effect.effect != 'produce': continue
            
            if len(effect.resources) != 1:
                if effect.resources[0][0] in COMMON_GOODS:
                    common_choices.append(effect.resources)

                else:
                    luxury_choices.append(effect.resources)

                continue

            if effect.resources[0][0] in COMMON_GOODS:
                for i in range(effect.resources[0][1]):
                    if effect.resources[0][0] in common_reqs:
                        common_reqs.remove(effect.resources[0][0])

            else:
                for i in range(effect.resources[0][1]):
                    if effect.resources[0][0] in luxury_reqs:
                        luxury_reqs.remove(effect.resources[0][0])

    def _activate_card(self, card: Card):
        for effect in card.effects:
            if effect.effect == "generate":
                resource_key, count = self._get_effect_resources(effect)
                resource = resource_map[resource_key]
                self.board[resource] += count
            else:
                self.effects[effect.effect].append(effect)

    def _do_payment(self, payment: Tuple[int, int, int]):
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
