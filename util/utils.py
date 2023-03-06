from __future__ import annotations

from typing import Tuple, List, Dict

from game.Card import Card, Effect
from util import ANSI
from util.constants import COMMON, LUXURY, TYPE_COLOR_MAP


def is_resource(effect: Effect) -> bool:
    return effect.card_type == COMMON or effect.card_type == LUXURY


def min_cost(payment_options: List[Tuple[int, int, int]]) -> str:
    if len(payment_options) == 0:
        return "-"
    return str(min(total_payment(payment) for payment in payment_options))


def total_payment(payment: Tuple[int, int, int]):
    return sum(payment)


def left_payment(payment: Tuple[int, int, int]):
    return payment[0]


def right_payment(payment: Tuple[int, int, int]):
    return payment[1]


def cards_as_string(cards: List[Card]) -> Tuple[str, Dict[Card, str]]:
    name = "Name"
    typ = "Type"
    effect = "Effect"
    resource = "Resource"

    max_name_len = len(name)
    max_type_len = len(typ)
    max_eff_len = len(effect)
    max_res_len = len(resource)

    for card in cards:
        max_name_len = max(max_name_len, len(card.name))
        max_type_len = max(max_type_len, len(card.card_type))
        max_eff_len = max(max_eff_len, len(card.effects_to_str()) - ANSI.ansilen(card.effects_to_str()))
        max_res_len = max(max_res_len, len(card.resource_to_str()))

    header = f"{name:{max_name_len}} | {typ:{max_type_len}} | {effect:{max_eff_len}} | {resource:{max_res_len}}"
    card_str_dict = dict()
    for card in cards:
        color = TYPE_COLOR_MAP[card.card_type] if card.card_type in TYPE_COLOR_MAP else ANSI.ANSI.BRIGHT_WHITE
        ansi_card_type = ANSI.use(color, card.card_type)
        card_str = f"{card.name:{max_name_len}} | " \
                   + f"{ansi_card_type:{max_type_len + ANSI.ansilen(ansi_card_type)}} | " \
                   + f"{card.effects_to_str():{max_eff_len + ANSI.ansilen(card.effects_to_str())}} | " \
                   + f"{card.resource_to_str():{max_res_len}} "
        card_str_dict[card] = card_str
    return header, card_str_dict
