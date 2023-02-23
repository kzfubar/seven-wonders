from typing import List, Tuple

from game.Card import Card
from game.CostCalculator import calculate_payment_options
from game.Flag import Flag
from game.Player import Player
from game.action.BuryAction import BURY
from game.action.CouponAction import COUPON
from game.action.DiscardAction import DISCARD
from game.action.FreeBuildAction import FREE_BUILD
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


async def end_round(player: Player):
    if Flag.DISCARD_BUILD in player.flags and player.flags[Flag.DISCARD_BUILD]:
        await _discard_build(player)


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
        if Flag.FREE_BUILD in player.flags and player.flags[Flag.FREE_BUILD]:
            player.display("Free build available!")
            actions.append(FREE_BUILD)
        player.display(", ".join([a.get_name() for a in actions]) + " a card: ")
        player_input = await player.get_input()
        action = player_input[0]
        arg = player_input[1::] if len(player_input) > 1 else None
        found_action = False
        for ac in actions:
            if action == ac.get_symbol():
                found_action = True
                turn_over = await ac.take_action(player, player.hand, arg)
                break
        if not found_action:
            player.display(f"Invalid action! {action}")
    player.display("turn over")


async def _discard_build(player: Player):
    all_players: List[Player] = [player]
    cur = player
    while not cur.neighbors[LEFT] == player:
        all_players.append(cur.neighbors[LEFT])
        cur = cur.neighbors[LEFT]
    all_discards: List[Card] = [card for p in all_players for card in p.discards]
    discard_str = display_cards(all_discards)
    player.display("\n".join(
        f"({i}) {discard_str[i]:80}"
        for i in range(len(all_discards))
    ))
    player.display("Free build from all previous discards: ")
    arg = (await player.get_input())[0::]
    await FREE_BUILD.take_action(player, all_discards, arg)
    del player.flags[Flag.DISCARD_BUILD]
