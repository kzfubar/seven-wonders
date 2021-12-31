import copy
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
        self.name: str = name
        self.wonder: Wonder = wonder
        self.hand: List[Card] = []
        self.board: DefaultDict[str, int] = defaultdict(int)
        self.board['coins'] = 3
        self.menu = Menu.Menu(self)
        self.turn_over: bool = True
        self.updates: List[str] = [] # update queue to display at start of player's turn
        self.discounts: DefaultDict[str, set] = defaultdict(set)
        self.next_coins: DefaultDict[str, int] = defaultdict(int)
        self.coupons: Set[Card] = set()
        self.effects: DefaultDict[str, List[Effect]] = defaultdict(list)
        self.neighbors: Dict[str, Optional[Player]] = {
            LEFT: None,
            RIGHT: None,
            'self': self
        }

        self.effects['produce'].append(Effect(effect='produce',
                                              resources=[(wonder.resource, 1)],
                                              target=[],
                                              direction=['self'],
                                              card_type='luxury' if wonder.resource in LUXURY_GOODS else 'common'))

        self.hand_payment_options: List[List[Tuple[int, int, int]]] = []
        self.wonder_payment_options: List[Tuple[int, int, int]] = []

    def __repr__(self):
        return f"Player{{wonder = {self.wonder}, \n" \
               f"board = {self.board}, \n" \
               f"hand = {self.hand}, \n" \
               f"effects = {self.effects}, \n"

    def __str__(self):  # todo make this nicer
        return f"wonder = {self.wonder} \n" \
               f"board = {self.board} \n" \
               f"effects = {self.effects}, \n" \
               f"neighbors = {self.neighbors[LEFT].name if self.neighbors[LEFT] is not None else 'NONE'} <-" \
               f" {self.name} -> " \
               f"{self.neighbors[RIGHT].name if self.neighbors[RIGHT] is not None else 'NONE'} \n"

    def set_game(self, game: Game):
        self.game = game

    @abstractmethod
    def display(self, message: Any):
        pass

    def _handle_input(self, player_input):
        action = player_input[0]
        args = player_input[1::] if len(player_input) > 1 else None
        self._take_action(action, args)

    def take_turn(self):
        self.turn_over = False
        self._calc_hand_costs()
        self.display('\n'.join(self.updates))
        self.updates = []
        self.display(self.discounts)
        self.display(f"You have {self.board['coins']} coins")
        self.display(f"Your hand is:\n{self._hand_to_str()}")
        self.display(f"Bury cost: {min_cost(self.wonder_payment_options)}")
        self._on_input(self._input_options(), self._handle_input)

    @abstractmethod
    def _on_input(self, message: str, callback) -> None:
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

    def run_military(self, age):
        for neighbor in (LEFT, RIGHT):
            if self.board['military_might'] > self.neighbors[neighbor].board['military_might']:
                self.board['military_points'] += MILITARY_POINTS[age]

            if self.board['military_might'] < self.neighbors[neighbor].board['military_might']:
                self.board['shame'] += 1

    def _hand_to_str(self) -> str:
        hand_str = display_cards(self.hand)
        return '\n'.join(f"({i}) {hand_str[i]:80} | Cost: {min_cost(payment_options)}"
                         for i, payment_options in enumerate(self.hand_payment_options))

    def _input_options(self) -> str:  # todo, we can check if other players are still taking their turn. also read the flag for free build
        if not self.turn_over:
            return "(p)lay, (d)iscard or (b)ury a card; or open the (m)enu: "
        return "turn over"

    def _handle_menu(self, player_input: str):
        args_list = player_input.split()
        menu_option = self.menu.options.get(args_list[0])
        self.display(menu_option.get_response(args_list[1:]))
        self._on_input(self._input_options(), self._handle_input)

    def _menu(self, args: Optional[str] = None) -> None:
        if not args:
            self.display(self.menu.get_options_str())
            self._on_input("select menu option: ", self._handle_menu)
        self._handle_menu(args)

    def _take_action(self, action: str, args: Optional[str] = None) -> None:
        if action == 'm':
            self._menu(args)
            return
        if args is None:
            self._on_input("please select a card: ", self._handle_input)
            return
        args = int(args)
        card = self.hand[args]
        if self.turn_over:
            self.display("turn over")
        elif action == 'p':
            self._play(card, self.hand_payment_options[args])
        elif action == 'd':
            self._discard(card)
        elif action == 'b':
            self._bury(card)
        else:
            self.display(f"Invalid action! {action}")  # todo allow for free build power
        self._on_input(self._input_options(), self._handle_input)

    def _play(self, card: Card, payment_options: List[Tuple[int, int, int]]) -> None:
        self.display(f"playing {card.name}")
        successfully_played = self._play_card(card, payment_options)
        if successfully_played:
            self.hand.remove(card)
        self.turn_over = successfully_played

    def _discard(self, card: Card) -> None:
        self.display(f"discarding {card}")
        self.board['coins'] += 3
        self.hand.remove(card)
        self.turn_over = True

    def _bury(self, card: Card) -> None:
        self.display(f"burying {card.name}")
        wonder_power = self.wonder.get_next_power()
        successfully_played = self._play_card(wonder_power, self.wonder_payment_options)
        if successfully_played:
            self.wonder.increment_level()
            self.hand.remove(card)
        self.turn_over = successfully_played

    def _play_card(self, card: Card, payment_options: List[Tuple[int, int, int]]) -> bool:
        if len(payment_options) == 0:
            self.display('card cannot be purchased')
            return False

        if payment_options[0][2] != 0:
            # cost is coins to bank
            self.handle_next_coins(-payment_options[0][2], 'spent')

        elif min_cost(payment_options) != '0': 
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

    def _get_payment_options(self, card: Card) -> List[Tuple[int, int, int]]:
        if card.name in self.coupons:
            return [(0, 0, 0)]

        if 'c' in card.cost:
            return [(0, 0, card.cost.count('c'))]

        luxury_reqs = [good for good in card.cost if good in LUXURY_GOODS]
        common_reqs = [good for good in card.cost if good in COMMON_GOODS]

        print(luxury_reqs, common_reqs)

        luxury_choices = simplify_cost_search(self.effects['produce'], luxury_reqs, LUXURY_GOODS)
        common_choices = simplify_cost_search(self.effects['produce'], common_reqs, COMMON_GOODS)

        left_effects = [effect for effect in self.neighbors[LEFT].effects['produce'] if effect.card_type in TRADABLE_TYPES]
        right_effects = [effect for effect in self.neighbors[RIGHT].effects['produce'] if effect.card_type in TRADABLE_TYPES]

        luxury_spread = find_resource_outcomes(left_effects, right_effects, luxury_choices, luxury_reqs, LUXURY_GOODS)
        common_spread = find_resource_outcomes(left_effects, right_effects, common_choices, common_reqs, COMMON_GOODS)


        options = set()

        for (lux_left, lux_right), (com_left, com_right) in itertools.product(luxury_spread, common_spread):

            options.add((lux_left * (1 if 'luxury' in self.discounts[LEFT] else 2) +
                         com_left * (1 if 'common' in self.discounts[LEFT] else 2),
                         lux_right * (1 if 'luxury' in self.discounts[RIGHT] else 2) +
                         com_right * (1 if 'common' in self.discounts[RIGHT] else 2),
                         0))

        # TODO: sort and slim down options
        return list(options)

    def _activate_card(self, card: Card):
        self.coupons |= set(card.coupons)

        for effect in card.effects:
            if effect.effect == "generate":
                resource_key, count = self._get_effect_resources(effect)
                resource = resource_map[resource_key]
                self.board[resource] += count

            elif effect.effect == "discount":
                for target, direction in itertools.product(effect.target, effect.direction):
                    self.discounts[direction].add(target)

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
        vp = defaultdict(int)
        vp['military'] = self.board["military_points"] - self.board['shame']
        vp['coins'] = self.board["coins"] // 3

        # covers wonder, civil, guild, and commercial cards
        for effect in self.effects["victory"]:
            if effect.target:
                for target, direction in itertools.product(effect.target, effect.direction):
                    vp[effect.card_type] += self.neighbors[direction].board[target] * effect.resources[0][1]

            else:
                vp[effect.card_type] += effect.resources[0][1]

        # calculate science
        science_counts = defaultdict(int)
        science_choices = []

        for effect in self.effects["research"]:
            if len(effect.resources) > 1:
                science_choices.append(tuple(resource[0] for resource in effect.resources))

            science_counts[effect.resources[0][0]] += 1

        for options in itertools.product([''], *science_choices):
            curr_counts = copy.copy(science_counts)

            for option in options[1:]:
                curr_counts[option] += 1
            
            vp['science'] = max(vp['science'],
                                min(curr_counts.values()) * 7 +
                                sum(count * count for count in curr_counts.values())
                                )

        return vp
