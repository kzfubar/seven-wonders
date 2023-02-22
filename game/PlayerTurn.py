from typing import List, Tuple

from game.CostCalculator import calculate_payment_options
from game.Player import Player
from game.action.BuryAction import BURY
from game.action.CouponAction import COUPON
from game.action.DiscardAction import DISCARD
from game.action.PlayAction import PLAY
from util.constants import LEFT, RIGHT, MILITARY_POINTS
from util.util import min_cost, display_cards


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
        calculate_payment_options(player, card) for card in player.hand
    ]
    wonder_payment_options = calculate_payment_options(
        player,
        player.wonder.get_next_power()
    )
    player.display("\n".join(player.updates))
    player.updates = []
    player.display(player.discounts)
    player.display(f"You have {player.board['coins']} coins")
    player.display(f"Your hand is:\n{_hand_to_str(player, hand_payment_options)}")
    player.display(f"Bury cost: {min_cost(wonder_payment_options)}")
    await _take_action(player)


def _hand_to_str(player: Player, hand_payment_options: List[List[Tuple[int, int, int]]]) -> str:
    hand_str = display_cards(player.hand)
    return "\n".join(
        f"({i}) {hand_str[i]:80} | Cost: {min_cost(payment_options)}"
        for i, payment_options in enumerate(hand_payment_options)
    )


async def _take_action(player: Player) -> None:
    actions = [PLAY, DISCARD, BURY]
    turn_over = False
    while not turn_over:
        if player.coupon_available():
            player.display("Coupon(s) available!: " + str(player.coupons))
            actions.append(COUPON)
        player.display(", ".join([a.get_name() for a in actions]) + " a card: ")
        player_input = await player.get_input()
        action = player_input[0]
        arg = player_input[1::] if len(player_input) > 1 else None
        found_action = False
        for ac in actions:
            if action == ac.get_symbol():
                found_action = True
                turn_over = await ac.take_action(player, arg)
                break
        if not found_action:
            player.display(f"Invalid action! {action}")  # todo allow for free build power
    player.display("turn over")
