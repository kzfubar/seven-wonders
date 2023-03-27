import asyncio
from typing import List, Dict

from game.Card import Card
from game.CostCalculator import calculate_payment_options
from game.Flag import Flag
from game.PaymentOption import PaymentOption
from game.Player import Player
from game.action.Actionable import Actionable
from game.action.BuryAction import BURY
from game.action.CouponAction import COUPON
from game.action.DiscardAction import DISCARD
from game.action.FreeBuildAction import FREE_BUILD
from game.action.PlayAction import PLAY
from util import ANSI
from util.constants import LEFT, RIGHT, MILITARY_POINTS_PER_AGE, DEFEAT, MILITARY_POINTS, GUILD
from util.toggles import DISPLAY_TYPE
from util.utils import min_cost, cards_as_string


def _hand_to_str(
        player: Player, hand_payment_options: Dict[Card, List[PaymentOption]]
) -> str:
    header, hand_str = cards_as_string(player.hand, player.toggles[DISPLAY_TYPE])
    max_len = ANSI.linelen(header)
    return (
            "    "
            + header
            + f" | {ANSI.use(ANSI.ANSI.BOLD, 'Cost')} \n"
            + "\n".join(
        f"({i}) {card_str:{max_len + ANSI.ansilen(card_str)}}| "
        + f"{'-' if min_cost(hand_payment_options[card]) == '' else min_cost(hand_payment_options[card]) + ' coins'}"
        for i, (card, card_str) in enumerate(hand_str.items())
    )
    )


def _to_event(player: Player,
              bury_options: List[PaymentOption],
              hand_options: Dict[Card, List[PaymentOption]]) -> Dict[str, Dict[str, List]]:
    play = {
        card.id: [p.as_tuple() for p in payments] for card, payments in hand_options.items()
    }
    discard = {
        card.id: [] for card, _ in hand_options.items()
    }
    bury = dict()
    if not player.wonder.is_max_level:
        bury = {
            player.wonder.get_next_stage().id: [p.as_tuple() for p in bury_options]
        }
    return {"play": play,
            "discard": discard,
            "bury": bury}


class PlayerActionPhase:
    def __init__(self, players):
        self.players = players
        self.actions: List[Actionable] = []

    async def select_actions(self):
        await asyncio.gather(
            *(self._select_action(player) for player in self.players)
        )

    def execute_actions(self):
        for actionable in self.actions:
            actionable.run()
        self.actions.clear()

    def run_military(self, player: Player, age):
        for direction in (LEFT, RIGHT):
            neighbor = player.neighbors[direction]
            if player.military_might() > neighbor.military_might():
                player.display(
                    f"you win against {neighbor.name}! you gain {MILITARY_POINTS_PER_AGE[age]}"
                )
                player.add_token(MILITARY_POINTS, MILITARY_POINTS_PER_AGE[age])

            elif player.military_might() < neighbor.military_might():
                player.display(f"you lost against {neighbor.name} - you gain 1 defeat!")
                player.add_token(DEFEAT, 1)

            else:
                player.display(f"you drew against {neighbor.name}!")

    async def _select_action(self, player: Player):
        player.status = "is taking their turn"
        player.event_update()
        hand_payment_options = {
            card: calculate_payment_options(player, card) for card in player.hand
        }

        wonder_payment_options: List[PaymentOption] = []
        if not player.wonder.is_max_level:
            wonder_payment_options = calculate_payment_options(
                player, player.wonder.get_next_stage()
            )

        player.cache_printout("\n".join(player.updates))
        player.updates = []
        player.cache_printout(f"{_hand_to_str(player, hand_payment_options)}")
        player.cache_printout(f"Bury cost: {min_cost(wonder_payment_options)}")
        player.cache_printout(f"You have {player.coins()} coins")

        actions = [PLAY, DISCARD, BURY]
        if player.wonder.is_max_level:
            actions.remove(BURY)
        available_coupons = player.available_coupons()
        if available_coupons:
            player.cache_printout("Coupon(s) available!: " + str(available_coupons))
            actions.append(COUPON)
        if Flag.FREE_BUILD in player.flags and player.flags[Flag.FREE_BUILD]:
            player.cache_printout("Free build available!")
            actions.append(FREE_BUILD)
        player.display_printouts()

        actionable = None
        while actionable is None:
            player.client.clear_message_buffer()
            player.client.send_event("game", {"type": "input",
                                              "options": _to_event(player,
                                                                   wonder_payment_options,
                                                                   hand_payment_options)})
            player_input = await player.get_input(
                ", ".join([a.get_name() for a in actions]) + " a card: "
            )
            action = player_input[0]
            arg = player_input[1::] if len(player_input) > 1 else None
            found_action = False
            for ac in actions:
                if action == ac.get_symbol():
                    found_action = True
                    actionable = await ac.select_card(player, player.hand, arg, self.players)
                    break
            if not found_action:
                player.display(f"Invalid action! {action}")
        self.actions.append(actionable)
        player.status = "has ended their turn"
        player.display("turn over")

    async def last_round(self, player: Player):
        player.clear_printouts()
        if Flag.PLAY_LAST in player.flags and player.flags[Flag.PLAY_LAST]:
            await self._select_action(player)

    async def end_round(self, player: Player):
        player.clear_printouts()
        if Flag.DISCARD_BUILD in player.flags and player.flags[Flag.DISCARD_BUILD]:
            await self._discard_build(player)

    async def end_age(self, player: Player, age: int) -> None:
        if age == 3 and Flag.GUILD_COPY in player.flags and player.flags[Flag.GUILD_COPY]:
            await self._guild_copy(player)
        player.enable_flags()

    async def _guild_copy(self, player: Player) -> None:
        left_guilds = [card for card in player.neighbors[LEFT].cards_played.keys() if card.card_type == GUILD]
        right_guilds = [card for card in player.neighbors[RIGHT].cards_played.keys() if card.card_type == GUILD]
        neighbor_guilds: List[Card] = left_guilds + right_guilds
        header, guild_str = cards_as_string(
            neighbor_guilds, player.toggles[DISPLAY_TYPE]
        )
        player.display("    " + header)
        player.display(
            "\n".join(
                f"({i}) {guild_str[card]:80}" for i, card in enumerate(neighbor_guilds)
            )
        )
        player.client.clear_message_buffer()
        arg = (await player.get_input("Copy a guild from your neighbors: "))[0::]
        await FREE_BUILD.select_card(player, neighbor_guilds, arg, self.players)
        del player.flags[Flag.GUILD_COPY]

    async def _discard_build(self, player: Player):
        all_discards: List[Card] = [card for p in self.players for card in p.discards]
        header, discard_str = cards_as_string(
            all_discards, player.toggles[DISPLAY_TYPE]
        )
        player.display("    " + header)
        player.display(
            "\n".join(
                f"({i}) {discard_str[card]:80}" for i, card in enumerate(all_discards)
            )
        )
        player.client.clear_message_buffer()
        arg = (await player.get_input("Free build from all previous discards: "))[0::]
        await FREE_BUILD.select_card(player, all_discards, arg, self.players)
        del player.flags[Flag.DISCARD_BUILD]
