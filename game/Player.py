
import math
from abc import abstractmethod
from collections import defaultdict
from typing import DefaultDict
from typing import Dict, Set, Any

from game import Menu
from game.Game import Game
from util.util import *


class Player:
    game: Game

    def __init__(self, name: str, wonder: Wonder):
        self.display(f"creating player {name} with {wonder.name}")
        self.name = name
        self.wonder = wonder
        self.hand = []
        self.board: DefaultDict[str, int] = defaultdict(int)
        self.board['coins'] = 3
        self.menu = Menu.Menu(self)
        self.turn_over = True
        self.updates = [] # update queue to display at start of player's turn

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

        self.next_coins: DefaultDict[str, int] = defaultdict(int)
        self.coupons: Set[Card] = set()
        self.effects: DefaultDict[str, List[Effect]] = defaultdict(list)
        self.neighbors: Dict[str, Optional[Player]] = {
            LEFT: None,
            RIGHT: None
        }

        self.effects['produce'].append(Effect(effect='produce',
                                              resources=[(wonder.resource, 1)],
                                              target=[],
                                              direction=['self'],
                                              card_type='luxury' if wonder.resource in LUXURY_GOODS else 'common'))

        self.hand_payment_options: List[List[Tuple[int, int, int]]]
        self.wonder_payment_options: List[Tuple[int, int, int]]

    def __repr__(self):
        return f"Player{{wonder = {self.wonder}, \n" \
               f"board = {self.board}, \n" \
               f"hand = {self.hand}, \n" \
               f"effects = {self.effects}, \n"

    def __str__(self):  # todo make this nicer
        return f"wonder = {self.wonder} \n" \
               f"board = {self.board} \n" \
               f"effects = {self.effects}, \n" \
               f"neighbors = L {self.neighbors[LEFT].name} {self.name} {self.neighbors[RIGHT].name} R \n"

    def set_game(self, game: Game):
        self.game = game

    @abstractmethod
    def display(self, message: Any):
        pass

    def _take_turn(self):
        self.turn_over = False
        self._calc_hand_costs()
        self.display('\n'.join(self.updates))
        self.updates = []

        self.display(f"You have {self.board['coins']} coins")
        self.display(f"Your hand is:\n{self._hand_to_str()}")
        self.display(f"Bury cost: {min_cost(self._get_payment_options(self.wonder.get_next_power()))}")
        while not self.turn_over:
            player_input = self._get_input("(p)lay, (d)iscard or (b)ury a card: ")   # todo let the player know that their turn has been accepted
            action = player_input[0]
            args = player_input[1::] if len(player_input) > 1 else None
            self.turn_over = self._take_action(action, args)

    @abstractmethod
    def take_turn(self):
        pass

    @abstractmethod
    def _get_input(self, message) -> str:
        pass

    def _calc_hand_costs(self) -> None:
        self.wonder_payment_options = self._get_payment_options(self.wonder.get_next_power())
        self.hand_payment_options = [self._get_payment_options(card) for card in self.hand]

    def handle_next_coins(self, coins: int, direction):
        self.next_coins[direction] += coins

    def update_coins(self):
        for k, v in self.next_coins.items():
            self.board['coins'] += v
            if k in (LEFT, RIGHT) and v != 0:
                self.updates.append(f'Received {v} coins from {self.neighbors[k].name}')
        self.next_coins = defaultdict(int)

    def _hand_to_str(self) -> str:
        hand_str = display_cards(self.hand)
        return '\n'.join(f"({i}) {hand_str[i]:80} | Cost: {min_cost(payment_options)}"
                         for i, payment_options in enumerate(self.hand_payment_options))

    def _menu(self, args: Optional[str] = None) -> bool:
        if not args:
            self.display(self.menu.get_options_str())
            args = self._get_input("select menu option: ")
        args_list = args.split()
        menu_option = self.menu.options.get(args_list[0])
        self.display(menu_option.get_response(args_list[1:]))
        return False

    def _take_action(self, action: str, args: Optional[str] = None) -> bool:
        if action == 'm':
            return self._menu(args)
        if args is None:
            args = self._get_input("please select a card: ")
        args = int(args)
        card = self.hand[args]

        if action == 'p':
            return self._play(card, self.hand_payment_options[args])
        elif action == 'd':
            return self._discard(card)
        elif action == 'b':
            return self._bury(card)
        else:
            self.display(f"Invalid action! {action}")
            return False

    def _play(self, card: Card, payment_options: List[Tuple[int, int, int]]) -> bool:
        self.display(f"playing {card.name}")
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
        if len(payment_options) == 0:
            self.display('card cannot be purchased')
            return False

        if payment_options[0][2] != 0:
            # cost is coins to bank
            self.handle_next_coins(-payment_options[0][2], 'spent')

        elif min_cost(payment_options) != 0: 
            # something has to be paid to a different player
            self._display_payment_options(payment_options)
            player_input = self._get_input("select a payment option: ")
            if player_input == 'q':
                return False
            # TODO: handle non int inputs/out of range??? (not just here)
            player_input = int(player_input)
            self._do_payment(payment_options[player_input])

        self._activate_card(card)
        self.board[card.card_type] += 1
        return True

    def _display_payment_options(self, payment_options):
        self.display("Payment options:")
        for i, option in enumerate(payment_options):
            self.display(f"({i}) {self.neighbors[LEFT].name} <- {option[0]}, {option[1]} -> {self.neighbors[RIGHT].name}")

    def _get_payment_options(self, card: Card) -> List[Tuple[int, int, int]]:  # todo consider coupons
        if card.name in self.coupons:
            return [(0, 0, 0)]

        if 'c' in card.cost:
            return [(0, 0, card.cost.count('c'))]

        luxury_reqs = [good for good in card.cost if good in LUXURY_GOODS]
        common_reqs = [good for good in card.cost if good in COMMON_GOODS]

        luxury_choices = simplify_cost_search(self.effects['produce'], luxury_reqs, LUXURY_GOODS)
        common_choices = simplify_cost_search(self.effects['produce'], common_reqs, COMMON_GOODS)

        left_effects = [effect for effect in self.neighbors[LEFT].effects['produce'] if effect.card_type in TRADABLE_TYPES]
        right_effects = [effect for effect in self.neighbors[RIGHT].effects['produce'] if effect.card_type in TRADABLE_TYPES]

        luxury_spread = find_resource_outcomes(left_effects, right_effects, luxury_choices, luxury_reqs, LUXURY_GOODS)
        common_spread = find_resource_outcomes(left_effects, right_effects, common_choices, common_reqs, COMMON_GOODS)


        options = set()

        # TODO: add discounts
        for a, b in itertools.product(luxury_spread, common_spread):
            options.add((2*(a[0] + b[0]), 2*(a[1] + b[1]), 0))

        # TODO: sort and slim down options
        return list(options)

    def _activate_card(self, card: Card):  # todo add a coupon
        self.coupons |= set(card.coupons)

        for effect in card.effects:
            if effect.effect == "generate":
                resource_key, count = self._get_effect_resources(effect)
                resource = resource_map[resource_key]
                self.board[resource] += count
            else:
                self.effects[effect.effect].append(effect)

    def _do_payment(self, payment: Tuple[int, int, int]):
        self.neighbors[LEFT].handle_next_coins(left_payment(payment), RIGHT)
        self.neighbors[RIGHT].handle_next_coins(right_payment(payment), LEFT)
        self.handle_next_coins(-1 * total_payment(payment), 'spent')  # -1 for decrement own coins

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
        cog, compass, tablet = 0, 0, 0
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
