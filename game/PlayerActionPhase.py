import asyncio
from typing import List, Tuple, Dict

from game.Card import Card
from game.CostCalculator import calculate_payment_options
from game.Flag import Flag
from game.Player import Player
from game.action.Actionable import Actionable
from game.action.BuryAction import BURY
from game.action.CouponAction import COUPON
from game.action.DiscardAction import DISCARD
from game.action.FreeBuildAction import FREE_BUILD
from game.action.PlayAction import PLAY
from util import ANSI
from util.constants import LEFT, RIGHT, MILITARY_POINTS, COINS
from util.utils import min_cost, cards_as_string


def _hand_to_str(
        player: Player, hand_payment_options: Dict[Card, List[Tuple[int, int, int]]]
) -> str:
    header, hand_str = cards_as_string(player.hand)
    max_len = ANSI.linelen(header)
    return "    " + header + " | Cost \n" + "\n".join(
        f"({i}) {card_str:{max_len + ANSI.ansilen(card_str)}}| {min_cost(hand_payment_options[card])} coins"
        for i, (card, card_str) in enumerate(hand_str.items())
    )


class PlayerActionPhase:
    def __init__(self, players):
        self.players = players
        self.actions: List[Actionable] = []

    async def select_actions(self):
        await asyncio.gather(*(self._select_action(player) for player in self.players))

    def execute_actions(self):
        for actionable in self.actions:
            actionable.run()
        self.actions.clear()

    def run_military(self, player: Player, age):
        for direction in (LEFT, RIGHT):
            neighbor = player.neighbors[direction]
            if player.board["military_might"] > neighbor.board["military_might"]:
                player.display(
                    f"you win against {neighbor.name}! you gain {MILITARY_POINTS[age]}"
                )
                player.board["military_points"] += MILITARY_POINTS[age]

            elif player.board["military_might"] < neighbor.board["military_might"]:
                player.display(f"you lost against {neighbor.name}! you gain 1 shame!")
                player.board["shame"] += 1

            else:
                player.display(f"you drew against {neighbor.name}!")

    async def _select_action(self, player: Player):
        hand_payment_options = {
            card: calculate_payment_options(player, card) for card in player.hand
        }

        if not player.wonder.is_max_level:
            wonder_payment_options = calculate_payment_options(
                player, player.wonder.get_next_power()
            )
        else:
            wonder_payment_options = []

        player.display("\n".join(player.updates))
        player.updates = []
        player.display(f"You have {player.board[COINS]} coins")
        player.display(f"{_hand_to_str(player, hand_payment_options)}")
        player.display(f"Bury cost: {min_cost(wonder_payment_options)}")

        actions = [PLAY, DISCARD, BURY]
        if player.wonder.is_max_level:
            actions.remove(BURY)
        available_coupons = player.available_coupons()
        if available_coupons:
            player.display("Coupon(s) available!: " + str(available_coupons))
            actions.append(COUPON)
        if Flag.FREE_BUILD in player.flags and player.flags[Flag.FREE_BUILD]:
            player.display("Free build available!")
            actions.append(FREE_BUILD)

        actionable = None
        while actionable is None:
            player_input = await player.get_input(
                ", ".join([a.get_name() for a in actions]) + " a card: "
            )
            action = player_input[0]
            arg = player_input[1::] if len(player_input) > 1 else None
            found_action = False
            for ac in actions:
                if action == ac.get_symbol():
                    found_action = True
                    actionable = await ac.select_card(player, player.hand, arg)
                    break
            if not found_action:
                player.display(f"Invalid action! {action}")
        self.actions.append(actionable)
        player.display("turn over")

    async def end_round(self, player: Player):
        if Flag.DISCARD_BUILD in player.flags and player.flags[Flag.DISCARD_BUILD]:
            await self._discard_build(player)

    async def _discard_build(self, player: Player):
        all_players: List[Player] = [player]
        cur = player
        while not cur.neighbors[LEFT] == player:
            all_players.append(cur.neighbors[LEFT])
            cur = cur.neighbors[LEFT]
        all_discards: List[Card] = [card for p in all_players for card in p.discards]
        header, discard_str = cards_as_string(all_discards)
        player.display("    " + header)
        player.display(
            "\n".join(f"({i}) {discard_str[card]:80}" for i, card in enumerate(all_discards))
        )
        arg = (await player.get_input("Free build from all previous discards: "))[0::]
        await FREE_BUILD.select_card(player, all_discards, arg)
        del player.flags[Flag.DISCARD_BUILD]
