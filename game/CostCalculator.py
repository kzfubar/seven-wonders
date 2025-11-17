import itertools
from typing import TYPE_CHECKING

from game.Card import Card, Effect
from game.PaymentOption import PaymentOption
from game.Player import Player
from util.constants import (
    COMMON,
    COMMON_GOODS,
    LEFT,
    LUXURY,
    LUXURY_GOODS,
    RIGHT,
    TRADABLE_TYPES,
)

if TYPE_CHECKING:
    from game.Resource import Resource


def calculate_payment_options(player: Player, card: Card) -> list[PaymentOption]:
    # this depends on the assumption that if a card has a cost, then there is no resource cost
    if "c" in card.cost:
        return [PaymentOption(bank_payment=card.cost.count("c"))]

    luxury_reqs = [good for good in card.cost if good in LUXURY_GOODS]
    common_reqs = [good for good in card.cost if good in COMMON_GOODS]

    luxury_choices, luxury_owned, luxury_reqs = simplify_cost_search(
        player.effects["produce"], luxury_reqs, LUXURY_GOODS
    )
    common_choices, common_owned, common_reqs = simplify_cost_search(
        player.effects["produce"], common_reqs, COMMON_GOODS
    )
    left, right = player.get_neighbors()

    left_effects = [
        effect
        for effect in left.effects["produce"]
        if effect.card_type in TRADABLE_TYPES
    ]
    right_effects = [
        effect
        for effect in right.effects["produce"]
        if effect.card_type in TRADABLE_TYPES
    ]

    luxury_spread = find_resource_outcomes(
        left_effects, right_effects, luxury_choices, luxury_reqs, LUXURY_GOODS
    )
    common_spread = find_resource_outcomes(
        left_effects, right_effects, common_choices, common_reqs, COMMON_GOODS
    )

    options: set[PaymentOption] = set()
    options.update(
        PaymentOption(
            common_owned=common_owned,
            lux_owned=luxury_owned,
            left_lux_cost=1 if LUXURY in player.discounts[LEFT] else 2,
            right_lux_cost=1 if LUXURY in player.discounts[RIGHT] else 2,
            left_common_cost=1 if COMMON in player.discounts[LEFT] else 2,
            right_common_cost=1 if COMMON in player.discounts[RIGHT] else 2,
            left_lux=list(left_lux),
            right_lux=list(right_lux),
            left_common=list(left_common),
            right_common=list(right_common),
        )
        for (left_lux, right_lux), (left_common, right_common) in itertools.product(
            luxury_spread, common_spread
        )
    )
    return sorted(options, key=lambda p: p.total())


def find_resource_outcomes(
    left_effects: list[Effect],
    right_effects: list[Effect],
    choices: list[tuple[str, ...]],
    reqs: list[str],
    goods: set[str],
) -> list[tuple[tuple[str, ...], tuple[str, ...]]]:
    outcomes: list[tuple[tuple[str, ...], tuple[str, ...]]] = []
    for options in itertools.product([""], *choices):
        reqs_curr: list[str] = reqs.copy()

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

            outcomes.append((tuple(left_reqs), tuple(right_reqs)))
    return outcomes


def valid_resources(choices: list[tuple[str, ...]], reqs: list[str]) -> bool:
    for options in itertools.product([""], *choices):
        reqs_curr: list[str] = reqs.copy()

        for option in options[1:]:
            if option in reqs_curr:
                reqs_curr.remove(option)

        if len(reqs_curr) == 0:
            return True

    return False


def simplify_cost_search(
    production_effects: list[Effect], reqs: list[str], goods: set[str]
) -> tuple[list[tuple[str, ...]], list[str], list[str]]:
    updated_reqs: list[str] = reqs.copy()
    need_purchase: list[tuple[str, ...]] = []
    self_owned: list[str] = []
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
