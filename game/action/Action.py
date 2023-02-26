import itertools
from abc import abstractmethod
from typing import List, Tuple, Optional

from game.Card import Card
from game.Flag import Flag
from game.Player import Player
from util.constants import LEFT, RIGHT, RESOURCE_MAP, COINS
from util.util import total_payment, left_payment, right_payment, min_cost


class Action:
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_symbol(self):
        pass

    @abstractmethod
    async def select_card(self, player: Player, cards: List[Card], arg: str) -> bool:
        pass


async def _get_card(player: Player, cards: List[Card], arg: Optional[str]) -> Optional[Card]:
    if arg is None:
        arg = await player.get_input("please select a card: ")
    try:
        arg = int(arg)
        return cards[arg]
    except ValueError:
        player.display("invalid argument!")
        return None
    except IndexError:
        player.display(f"{arg} is out of range!")
        return None


async def _select_payment_option(player: Player, payment_options: List[Tuple[int, int, int]]) -> bool:
    if len(payment_options) == 0:
        player.display("card cannot be purchased")
        return False

    if payment_options[0][2] != 0:
        # cost is coins to bank
        payment = payment_options[0][2]
        if not _valid_payment(player, payment):
            player.display("Cannot afford this card")
            return False
        player.handle_next_coins(-payment_options[0][2], "spent")

    elif min_cost(payment_options) != "0":
        # something has to be paid to a different player
        _display_payment_options(player, payment_options)
        player_input = await player.get_input("select a payment option: ")
        if player_input == "q":
            return False
        player_input = int(player_input)
        if player_input > len(payment_options):
            player.display("out of range!")
            return False
        payment = payment_options[player_input][0] + payment_options[player_input][1]
        if not _valid_payment(player, payment):
            player.display("Cannot afford this payment")
            return False
        _do_payment(player, payment_options[player_input])
    return True


def _display_payment_options(player: Player, payment_options: List[Tuple[int, int, int]]):
    player.display("Payment options:")
    for i, option in enumerate(payment_options):
        player.display(
            f"({i}) {player.neighbors[LEFT].name} <- {option[0]}, {option[1]} -> {player.neighbors[RIGHT].name}"
        )


def _activate_card(player: Player, card: Card):
    player.board[card.card_type] += 1
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

        elif effect.effect == "discard_build":
            player.flags[Flag.DISCARD_BUILD] = True

        else:
            player.effects[effect.effect].append(effect)


def _do_payment(player: Player, payment_option: Tuple[int, int, int]):
    player.neighbors[LEFT].handle_next_coins(left_payment(payment_option), RIGHT)
    player.neighbors[RIGHT].handle_next_coins(right_payment(payment_option), LEFT)
    player.handle_next_coins(
        -1 * total_payment(payment_option), "spent"
    )  # -1 for decrement own coins


def _valid_payment(player: Player, payment: int) -> bool:
    return payment <= player.board[COINS]
