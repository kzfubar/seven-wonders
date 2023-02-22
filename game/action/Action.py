import itertools
from abc import abstractmethod
from typing import List, Tuple, Optional

from game.Card import Card
from game.Flag import Flag
from game.Player import Player
from util.constants import LEFT, RIGHT, RESOURCE_MAP
from util.util import total_payment, left_payment, right_payment, min_cost


class Action:
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_symbol(self):
        pass

    @abstractmethod
    async def take_action(self, player: Player, arg: str) -> bool:
        pass


async def _get_card(player: Player, arg: Optional[str]) -> Optional[Card]:
    if arg is None:
        player.display("please select a card: ")
        arg = await player.get_input()
    arg = int(arg)
    if arg >= len(player.hand):
        player.display("out of range!")
        return None
    return player.hand[arg]


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
        player_input = await player.get_input()
        if player_input == "q":
            return False
        player_input = int(player_input)
        if player_input > len(payment_options):
            player.display("out of range!")
            return False
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


def _activate_card(player: Player, card: Card):
    player.add_coupons(set(card.coupons))

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

        elif effect.effect == "free_build":
            player.flags[Flag.FREE_BUILD] = True

        else:
            player.effects[effect.effect].append(effect)


def _do_payment(player: Player, payment: Tuple[int, int, int]):
    player.neighbors[LEFT].handle_next_coins(left_payment(payment), RIGHT)
    player.neighbors[RIGHT].handle_next_coins(right_payment(payment), LEFT)
    player.handle_next_coins(
        -1 * total_payment(payment), "spent"
    )  # -1 for decrement own coins
