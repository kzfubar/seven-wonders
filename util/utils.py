from __future__ import annotations

from typing import Tuple, List, Dict

from game.Card import Card, Effect
from game.PaymentOption import PaymentOption
from util.ANSI import ansilen, linelen, use, ANSI
from util.constants import COMMON, LUXURY


def is_resource(effect: Effect) -> bool:
    return effect.card_type == COMMON or effect.card_type == LUXURY


def min_cost(payment_options: List[PaymentOption]) -> str:
    if len(payment_options) == 0:
        return ""
    return str(min(payment.total() for payment in payment_options))

def cards_as_string(
    cards: List[Card], display_type: bool
) -> Tuple[str, Dict[Card, str]]:
    name = use(ANSI.BOLD, "Name")
    typ = use(ANSI.BOLD, "Type")
    effect = use(ANSI.BOLD, "Effect")
    resource = use(ANSI.BOLD, "Resource")
    coupon = use(ANSI.BOLD, "Coupons")

    max_name_len = linelen(name)
    max_type_len = linelen(typ)
    max_eff_len = linelen(effect)
    max_res_len = linelen(resource)
    max_coup_len = linelen(coupon)

    for card in cards:
        max_name_len = max(max_name_len, len(card.name))
        max_type_len = max(max_type_len, len(card.card_type))
        max_eff_len = max(max_eff_len, linelen(card.effects_to_str()))
        max_res_len = max(max_res_len, len(card.resource_to_str()))
        max_coup_len = max(max_coup_len, len(', '.join([c.name for c in card.coupons])))

    header = (
        f"{name:{max_name_len + ansilen(name)}} | "
        + (f"{typ:{max_type_len + ansilen(typ)}} | " if display_type else "")
        + f"{effect:{max_eff_len + ansilen(effect)}} | "
        + f"{resource:{max_res_len + ansilen(resource)}} | "
        + f"{coupon:{max_coup_len + ansilen(coupon)}}"
    )
    card_str_dict = dict()
    for card in cards:
        card_name = card.with_color(card.name)
        type_name = card.with_color(card.card_type)
        coupon_names = ', '.join([c.with_color(c.name) for c in card.coupons])
        card_str = (
            f"{card_name:{max_name_len + ansilen(card_name)}} | "
            + (
                f"{type_name:{max_type_len + ansilen(type_name)}} | "
                if display_type
                else ""
            )
            + f"{card.effects_to_str():{max_eff_len + ansilen(card.effects_to_str())}} | "
            + f"{card.resource_to_str():{max_res_len}} | "
            + f"{coupon_names:{max_coup_len + ansilen(coupon_names)}} "
        )
        card_str_dict[card] = card_str
    return header, card_str_dict
