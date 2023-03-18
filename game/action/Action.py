import itertools
from abc import abstractmethod
from typing import List, Optional

from game.Card import Card
from game.Flag import Flag
from game.PaymentOption import PaymentOption
from game.Player import Player
from networking.messaging.messageUtil import GAME
from util.constants import LEFT, RIGHT, RESOURCE_MAP
from util.utils import min_cost


class Action:
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_symbol(self):
        pass

    @abstractmethod
    async def select_card(
            self, player: Player, cards: List[Card], arg: str, players: List[Player]
    ) -> bool:
        pass


async def _get_card(
        player: Player, cards: List[Card], arg: Optional[str]
) -> Optional[Card]:
    if arg is None:
        player.client.clear_message_buffer()
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


async def _select_payment_option(
        player: Player,
        played_card: Card,
        payment_options: List[PaymentOption]
) -> bool:
    if len(payment_options) == 0:
        player.display("card cannot be purchased")
        return False

    payment = 0
    bank_payment = payment_options[0].bank_payment
    if bank_payment != 0:
        # cost is coins to bank
        payment = bank_payment
        if not _valid_payment(player, bank_payment):
            player.display("Cannot afford this card")
            return False
        player.handle_next_coins(-bank_payment, "spent")

    elif min_cost(payment_options) != "0":
        # something has to be paid to a different player
        _display_payment_options(player, payment_options)
        player.client.clear_message_buffer()
        player.client.send_event(GAME, {"type": "payment", "options": [i for i, _ in enumerate(payment_options)]})
        player_input = await player.get_input("select a payment option: ")
        if player_input == "q":
            return False
        player_input = int(player_input)
        if player_input > len(payment_options):
            player.display("out of range!")
            return False
        try:
            payment = payment_options[player_input].total()
            if not _valid_payment(player, payment):
                player.display("Cannot afford this payment")
                return False
            _do_payment(player, payment_options[player_input])
        except Exception:
            player.display(f"Failed to pay {player_input}")
            return False
    player.cards_played[played_card] = {"cost": payment}
    return True


def _display_payment_options(
        player: Player, payment_options: List[PaymentOption]
):
    player.display("Payment options:")
    for i, option in enumerate(payment_options):
        player.display(
            f"({i}) {player.neighbors[LEFT].name} <- {option.left_payment}, {option.right_payment} -> {player.neighbors[RIGHT].name}"
        )


def _activate_card(player: Player, card: Card):
    player.add_coupons(set(card.coupons))
    for effect in card.effects:
        player.effects_id_to_card[effect.effect_id] = card
        if effect.effect == "generate":
            resource_key, count = player.get_effect_resources(effect)
            player.effects[effect.effect].append(effect)
            player.add_token(RESOURCE_MAP[resource_key], count)

        elif effect.effect == "discount":
            for target, direction in itertools.product(effect.target, effect.direction):
                player.discounts[direction].add(target)

        elif effect.effect == "free_build":
            player.flags[Flag.FREE_BUILD] = True

        elif effect.effect == "discard_build":
            player.flags[Flag.DISCARD_BUILD] = True

        else:
            player.effects[effect.effect].append(effect)


def _do_payment(player: Player, payment_option: PaymentOption):
    player.neighbors[LEFT].handle_next_coins(payment_option.left_payment, RIGHT)
    player.neighbors[RIGHT].handle_next_coins(payment_option.right_payment, LEFT)

    for owned in payment_option.common_owned:
        player.coins_gained[owned] += 2
    for owned in payment_option.lux_owned:
        player.coins_gained[owned] += 2

    for lux in payment_option.left_lux:
        player.neighbors[LEFT].coins_gained[lux] += payment_option.left_lux_cost
        if payment_option.left_lux_cost == 1:
            player.discount_coins_saved["luxury"][LEFT] += len(payment_option.left_lux) * payment_option.left_lux_cost
    for common in payment_option.left_common:
        player.neighbors[LEFT].coins_gained[common] += payment_option.left_common_cost
        if payment_option.left_common_cost == 1:
            player.discount_coins_saved["common"][LEFT] += len(payment_option.left_common) * payment_option.left_common_cost
    for lux in payment_option.right_lux:
        player.neighbors[RIGHT].coins_gained[lux] += payment_option.right_lux_cost
        if payment_option.right_lux_cost == 1:
            player.discount_coins_saved["luxury"][RIGHT] += len(payment_option.right_lux) * payment_option.right_lux_cost
    for common in payment_option.right_common:
        player.neighbors[RIGHT].coins_gained[common] += payment_option.right_common_cost
        if payment_option.right_common_cost == 1:
            player.discount_coins_saved["common"][RIGHT] += len(payment_option.right_common) * payment_option.right_common_cost

    # -1 for decrement own coins
    player.handle_next_coins(-1 * payment_option.total(), "spent")


def _valid_payment(player: Player, payment: int) -> bool:
    return payment <= player.coins()


def _announce(msg: str, players: List[Player]):
    for player in players:
        player.display(msg)
