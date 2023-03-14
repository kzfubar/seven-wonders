import itertools
from typing import List, Set, Tuple

from game.Card import Card
from game.PaymentOption import PaymentOption, payment, bank_payment
from game.Player import Player
from util.constants import (
    COMMON,
    COMMON_GOODS,
    LUXURY,
    LUXURY_GOODS,
    LEFT,
    TRADABLE_TYPES,
    RIGHT,
)


def calculate_payment_options(player: Player, card: Card) -> List[PaymentOption]:
    # this depends on the assumption that if a card has a cost, then there is no resource cost
    if "c" in card.cost:
        return [bank_payment(card.cost.count("c"))]

    luxury_reqs = [good for good in card.cost if good in LUXURY_GOODS]
    common_reqs = [good for good in card.cost if good in COMMON_GOODS]

    luxury_choices = simplify_cost_search(
        player.effects["produce"], luxury_reqs, LUXURY_GOODS
    )
    common_choices = simplify_cost_search(
        player.effects["produce"], common_reqs, COMMON_GOODS
    )

    left_effects = [
        effect
        for effect in player.neighbors[LEFT].effects["produce"]
        if effect.card_type in TRADABLE_TYPES
    ]
    right_effects = [
        effect
        for effect in player.neighbors[RIGHT].effects["produce"]
        if effect.card_type in TRADABLE_TYPES
    ]

    luxury_spread = find_resource_outcomes(
        left_effects, right_effects, luxury_choices, luxury_reqs, LUXURY_GOODS
    )
    common_spread = find_resource_outcomes(
        left_effects, right_effects, common_choices, common_reqs, COMMON_GOODS
    )

    options: Set[PaymentOption] = set()
    for (lux_left, lux_right), (com_left, com_right) in itertools.product(luxury_spread, common_spread):
        l_payment = lux_left * (1 if LUXURY in player.discounts[LEFT] else 2) \
                    + com_left * (1 if COMMON in player.discounts[LEFT] else 2)
        r_payment = lux_right * (1 if LUXURY in player.discounts[RIGHT] else 2) \
                    + com_right * (1 if COMMON in player.discounts[RIGHT] else 2)
        options.add((payment(l_payment=l_payment, r_payment=r_payment)))
    return sorted(list(options), key=lambda p: p.total())


def find_resource_outcomes(left_effects, right_effects, choices, reqs, goods) -> Set[Tuple]:
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
                continue

            if not valid_resources(
                    simplify_cost_search(right_effects, right_reqs, goods), right_reqs
            ):
                continue

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


def simplify_cost_search(production_effects, reqs, goods):
    choices = []

    for production in production_effects:
        if len(production.resources) != 1:
            if production.resources[0].key in goods:
                choices.append(tuple(resource.key for resource in production.resources))

        else:
            for _ in range(production.resources[0].amount):
                if production.resources[0].key not in reqs:
                    break

                reqs.remove(production.resources[0].key)

    return choices
