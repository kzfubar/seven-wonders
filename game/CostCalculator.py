import itertools
from typing import List, Set, Tuple

from game.Card import Card
from game.PaymentOption import PaymentOption
from game.Player import Player
from game.Resource import Resource
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
    if f"c" in card.cost:
        return [PaymentOption(bank_payment=card.cost.count("c"))]

    luxury_reqs = [good for good in card.cost if good in LUXURY_GOODS]
    common_reqs = [good for good in card.cost if good in COMMON_GOODS]

    luxury_choices, luxury_owned, luxury_reqs = simplify_cost_search(
        player.effects["produce"], luxury_reqs, LUXURY_GOODS
    )
    common_choices, common_owned, common_reqs = simplify_cost_search(
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
    for (left_lux, right_lux), (left_common, right_common) in itertools.product(
        luxury_spread, common_spread
    ):
        options.add(
            PaymentOption(
                common_owned=common_owned,
                lux_owned=luxury_owned,
                left_lux_cost=1 if LUXURY in player.discounts[LEFT] else 2,
                right_lux_cost=1 if LUXURY in player.discounts[RIGHT] else 2,
                left_common_cost=1 if COMMON in player.discounts[LEFT] else 2,
                right_common_cost=1 if COMMON in player.discounts[RIGHT] else 2,
                left_lux=left_lux,
                right_lux=right_lux,
                left_common=left_common,
                right_common=right_common,
            )
        )
    return sorted(list(options), key=lambda p: p.total())


def find_resource_outcomes(
    left_effects, right_effects, choices, reqs, goods
) -> Set[Tuple[Tuple[str], Tuple[str]]]:
    outcomes = list()
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

            left_purchase, _, updated_left_reqs = simplify_cost_search(
                left_effects, left_reqs, goods
            )
            if not valid_resources(left_purchase, updated_left_reqs):
                continue

            right_purchase, _, updated_right_reqs = simplify_cost_search(
                right_effects, right_reqs, goods
            )
            if not valid_resources(right_purchase, updated_right_reqs):
                continue

            outcomes.append((left_reqs, right_reqs))
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
    updated_reqs = reqs.copy()
    need_purchase = []
    self_owned = []
    for production in production_effects:
        resource: Resource = production.resources[0]
        if len(production.resources) != 1:
            if resource.key in goods:
                need_purchase.append(tuple(r.key for r in production.resources))

        else:
            for _ in range(resource.amount):
                if resource.key not in updated_reqs:
                    break
                updated_reqs.remove(resource.key)
                self_owned.append(resource.key)

    return need_purchase, self_owned, updated_reqs
