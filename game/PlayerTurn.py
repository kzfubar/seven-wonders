import itertools
from typing import List, Tuple

from game.Card import Card
from game.Player import Player
from util.constants import LUXURY_GOODS, COMMON_GOODS, LEFT, TRADABLE_TYPES, RIGHT, RESOURCE_MAP, MILITARY_POINTS
from util.util import min_cost, simplify_cost_search, find_resource_outcomes, display_cards, left_payment, \
    right_payment, total_payment


def run_military(player: Player, age):
    for neighbor in (LEFT, RIGHT):
        if (
                player.board["military_might"]
                > player.neighbors[neighbor].board["military_might"]
        ):
            player.board["military_points"] += MILITARY_POINTS[age]

        if (
                player.board["military_might"]
                < player.neighbors[neighbor].board["military_might"]
        ):
            player.board["shame"] += 1


async def take_turn(player: Player):
    hand_payment_options = [
        _calc_payment_options(player, card) for card in player.hand
    ]
    wonder_payment_options = _calc_payment_options(
        player,
        player.wonder.get_next_power()
    )
    player.display("\n".join(player.updates))
    player.updates = []
    player.display(player.discounts)
    player.display(f"You have {player.board['coins']} coins")
    player.display(f"Your hand is:\n{_hand_to_str(player, hand_payment_options)}")
    player.display(f"Bury cost: {min_cost(wonder_payment_options)}")
    await _take_action(player, hand_payment_options, wonder_payment_options)


def _calc_payment_options(self, card: Card) -> List[Tuple[int, int, int]]:
    if card.name in self.coupons:
        return [(0, 0, 0)]

    if "c" in card.cost:
        return [(0, 0, card.cost.count("c"))]

    luxury_reqs = [good for good in card.cost if good in LUXURY_GOODS]
    common_reqs = [good for good in card.cost if good in COMMON_GOODS]

    print(luxury_reqs, common_reqs)

    luxury_choices = simplify_cost_search(
        self.effects["produce"], luxury_reqs, LUXURY_GOODS
    )
    common_choices = simplify_cost_search(
        self.effects["produce"], common_reqs, COMMON_GOODS
    )

    left_effects = [
        effect
        for effect in self.neighbors[LEFT].effects["produce"]
        if effect.card_type in TRADABLE_TYPES
    ]
    right_effects = [
        effect
        for effect in self.neighbors[RIGHT].effects["produce"]
        if effect.card_type in TRADABLE_TYPES
    ]

    luxury_spread = find_resource_outcomes(
        left_effects, right_effects, luxury_choices, luxury_reqs, LUXURY_GOODS
    )
    common_spread = find_resource_outcomes(
        left_effects, right_effects, common_choices, common_reqs, COMMON_GOODS
    )

    options = set()

    for (lux_left, lux_right), (com_left, com_right) in itertools.product(
            luxury_spread, common_spread
    ):
        options.add(
            (
                lux_left * (1 if "luxury" in self.discounts[LEFT] else 2)
                + com_left * (1 if "common" in self.discounts[LEFT] else 2),
                lux_right * (1 if "luxury" in self.discounts[RIGHT] else 2)
                + com_right * (1 if "common" in self.discounts[RIGHT] else 2),
                0,
            )
        )

    # TODO: sort and slim down options
    return list(options)


def _hand_to_str(player: Player, hand_payment_options: List[List[Tuple[int, int, int]]]) -> str:
    hand_str = display_cards(player.hand)
    return "\n".join(
        f"({i}) {hand_str[i]:80} | Cost: {min_cost(payment_options)}"
        for i, payment_options in enumerate(hand_payment_options)
    )


async def _take_action(player: Player,
                       hand_payment_options: List[List[Tuple[int, int, int]]],
                       wonder_payment_options: List[Tuple[int, int, int]]) -> None:
    turn_over = False
    while not turn_over:
        player.display("(p)lay, (d)iscard or (b)ury a card: ")
        player_input = await _get_input(player)
        action = player_input[0]
        args = player_input[1::] if len(player_input) > 1 else None
        if args is None:
            player.display("please select a card: ")
            continue
        args = int(args)
        card = player.hand[args]
        if action == "p":
            turn_over = await _play(player, card, hand_payment_options[args])
        elif action == "d":
            turn_over = _discard(player, card)
        elif action == "b":
            turn_over = await _bury(player, card, wonder_payment_options)
        else:
            player.display(f"Invalid action! {action}")  # todo allow for free build power
    player.display("turn over")


async def _play(player: Player, card: Card, payment_options: List[Tuple[int, int, int]]) -> bool:
    player.display(f"playing {card.name}")
    successfully_played = await _play_card(player, card, payment_options)
    if successfully_played:
        player.hand.remove(card)
    return successfully_played


def _discard(player: Player, card: Card) -> bool:
    player.display(f"discarding {card}")
    player.board["coins"] += 3
    player.hand.remove(card)
    return True


async def _bury(player: Player, card: Card, wonder_payment_options: List[Tuple[int, int, int]]) -> bool:
    player.display(f"burying {card.name}")
    wonder_power = player.wonder.get_next_power()
    successfully_played = await _play_card(player, wonder_power, wonder_payment_options)
    if successfully_played:
        player.wonder.increment_level()
        player.hand.remove(card)
    return successfully_played


async def _play_card(player: Player, card: Card, payment_options: List[Tuple[int, int, int]]) -> bool:
    if len(payment_options) == 0:
        player.display("card cannot be purchased")
        return False

    if payment_options[0][2] != 0:
        # cost is coins to bank
        player.handle_next_coins(-payment_options[0][2], "spent")

    elif min_cost(payment_options) != "0":
        # something has to be paid to a different player
        _display_payment_options(player, payment_options)
        player.display("select a payment option: ")
        player_input = await _get_input(player)
        if player_input == "q":
            return False
        # TODO: handle non int inputs/out of range??? (not just here)
        player_input = int(player_input)
        _do_payment(player, payment_options[player_input])

    _activate_card(player, card)
    player.board[card.card_type] += 1
    return True


def _display_payment_options(player: Player, payment_options: List[Tuple[int, int, int]]):
    player.display("Payment options:")
    for i, option in enumerate(payment_options):
        player.display(
            f"({i}) {player.neighbors[LEFT].name} <- {option[0]}, {option[1]} -> {player.neighbors[RIGHT].name}"
        )


async def _get_input(player: Player) -> str:
    return await player.client.get_message()


def _do_payment(player: Player, payment: Tuple[int, int, int]):
    player.neighbors[LEFT].handle_next_coins(left_payment(payment), RIGHT)
    player.neighbors[RIGHT].handle_next_coins(right_payment(payment), LEFT)
    player.handle_next_coins(
        -1 * total_payment(payment), "spent"
    )  # -1 for decrement own coins


def _activate_card(player: Player, card: Card):
    player.coupons |= set(card.coupons)

    for effect in card.effects:
        if effect.effect == "generate":
            resource_key, count = player.get_effect_resources(effect)
            resource = RESOURCE_MAP[resource_key]
            player.board[resource] += count

        elif effect.effect == "discount":
            for target, direction in itertools.product(
                    effect.target, effect.direction
            ):
                player.discounts[direction].add(target)

        else:
            player.effects[effect.effect].append(effect)
