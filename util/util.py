from __future__ import annotations

from typing import Tuple, List
import itertools

from game.Card import Card, Effect


def is_resource(effect: Effect) -> bool:
    return effect.card_type == "common" or effect.card_type == "luxury"


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


def simplify_cost_search(effects, reqs, goods):
    choices = []

    for effect in effects:
        if len(effect.resources) != 1:
            if effect.resources[0][0] in goods:
                choices.append(tuple(resource[0] for resource in effect.resources))

        else:
            for _ in range(effect.resources[0][1]):
                if effect.resources[0][0] not in reqs:
                    break

                reqs.remove(effect.resources[0][0])

    return choices


def find_resource_outcomes(left_effects, right_effects, choices, reqs, goods):
    outcomes = set()
    for options in itertools.product([""], *choices):

        reqs_curr = reqs[:]

        for option in options[1:]:
            if option in reqs_curr:
                reqs_curr.remove(option)

        for i in range(1 << len(reqs_curr)):
            left_reqs = []
            right_reqs = []

            for j, val in enumerate(reqs_curr):
                if i & (1 << j) == 0:
                    left_reqs.append(val)
                else:
                    right_reqs.append(val)

            l_count, r_count = len(left_reqs), len(right_reqs)
            if (l_count, r_count) in outcomes:
                continue

            if not valid_resources(
                simplify_cost_search(left_effects, left_reqs, goods), left_reqs
            ):
                break

            if not valid_resources(
                simplify_cost_search(right_effects, right_reqs, goods), right_reqs
            ):
                break

            outcomes.add((l_count, r_count))
    return outcomes


def valid_resources(choices, reqs):
    for options in itertools.product([""], *choices):

        reqs_curr = reqs[:]

        for option in options[1:]:
            if option in reqs_curr:
                reqs_curr.remove(option)

        if len(reqs_curr) == 0:
            return True

    return False


def display_cards(cards: List[Card]) -> List[str]:
    max_name_len = 0
    max_type_len = 0
    max_effect_len = 0
    max_resource_len = 0

    for card in cards:
        max_name_len = max(max_name_len, len(card.name))
        max_type_len = max(max_type_len, len(card.card_type))
        max_effect_len = max(max_effect_len, len(card.effects_to_str()))
        max_resource_len = max(max_resource_len, len(card.resource_to_str()))

    return [
        f"{card.name:{max_name_len}} | "
        f"{card.card_type:{max_type_len}} | "
        f"{card.effects_to_str():{max_effect_len}} |"
        f" {card.resource_to_str():{max_resource_len}}"
        for card in cards
    ]
