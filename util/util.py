from __future__ import annotations

from typing import Tuple, List, Dict

from game.Card import Card, Effect
from util.constants import COMMON, LUXURY


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


def cards_as_string(cards: List[Card]) -> Dict[Card, str]:
    max_name_len = 0
    max_type_len = 0
    max_effect_len = 0
    max_resource_len = 0

    for card in cards:
        max_name_len = max(max_name_len, len(card.name))
        max_type_len = max(max_type_len, len(card.card_type))
        max_effect_len = max(max_effect_len, len(card.effects_to_str()))
        max_resource_len = max(max_resource_len, len(card.resource_to_str()))

    return {card: f"{card.name:{max_name_len}} | "
                  + f"{card.card_type:{max_type_len}} | "
                  + f"{card.effects_to_str():{max_effect_len}} | "
                  + f"{card.resource_to_str():{max_resource_len}} "
            for card in cards}
