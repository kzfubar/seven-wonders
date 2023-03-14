from __future__ import annotations

from typing import Tuple, List, Dict

from game.Card import Card, Effect
from game.PaymentOption import PaymentOption
from util import ANSI
from util.constants import COMMON, LUXURY, TYPE_COLOR_MAP


def is_resource(effect: Effect) -> bool:
    return effect.card_type == COMMON or effect.card_type == LUXURY


def min_cost(payment_options: List[PaymentOption]) -> str:
    if len(payment_options) == 0:
        return ""
    return str(min(payment.total() for payment in payment_options))

def cards_as_string(
    cards: List[Card], display_type: bool
) -> Tuple[str, Dict[Card, str]]:
    name = ANSI.use(ANSI.ANSI.BOLD, "Name")
    typ = ANSI.use(ANSI.ANSI.BOLD, "Type")
    effect = ANSI.use(ANSI.ANSI.BOLD, "Effect")
    resource = ANSI.use(ANSI.ANSI.BOLD, "Resource")

    max_name_len = ANSI.linelen(name)
    max_type_len = ANSI.linelen(typ)
    max_eff_len = ANSI.linelen(effect)
    max_res_len = ANSI.linelen(resource)

    for card in cards:
        max_name_len = max(max_name_len, len(card.name))
        max_type_len = max(max_type_len, len(card.card_type))
        max_eff_len = max(max_eff_len, ANSI.linelen(card.effects_to_str()))
        max_res_len = max(max_res_len, len(card.resource_to_str()))

    header = (
        f"{name:{max_name_len + ANSI.ansilen(name)}} | "
        + (f"{typ:{max_type_len + ANSI.ansilen(typ)}} | " if display_type else "")
        + f"{effect:{max_eff_len + ANSI.ansilen(effect)}} | "
        + f"{resource:{max_res_len + ANSI.ansilen(resource)}}"
    )
    card_str_dict = dict()
    for card in cards:
        color = (
            TYPE_COLOR_MAP[card.card_type]
            if card.card_type in TYPE_COLOR_MAP
            else ANSI.ANSI.BRIGHT_WHITE
        )
        ansi_card_name = ANSI.use(color, card.name)
        ansi_card_type = ANSI.use(color, card.card_type)
        card_str = (
            f"{ansi_card_name:{max_name_len + ANSI.ansilen(ansi_card_name)}} | "
            + (
                f"{ansi_card_type:{max_type_len + ANSI.ansilen(ansi_card_type)}} | "
                if display_type
                else ""
            )
            + f"{card.effects_to_str():{max_eff_len + ANSI.ansilen(card.effects_to_str())}} | "
            + f"{card.resource_to_str():{max_res_len}} "
        )
        card_str_dict[card] = card_str
    return header, card_str_dict
