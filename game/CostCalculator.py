import itertools
from typing import List, Tuple

from game.Card import Card
from game.Player import Player
from util.constants import COMMON_GOODS, LUXURY_GOODS, LEFT, TRADABLE_TYPES, RIGHT
from util.util import simplify_cost_search, find_resource_outcomes


def calculate_payment_options(player: Player, card: Card) -> List[Tuple[int, int, int]]:
    # this depends on the assumption that if a card has a cost, then there is no resource cost
    if "c" in card.cost:
        return [(0, 0, card.cost.count("c"))]

    luxury_reqs = [good for good in card.cost if good in LUXURY_GOODS]
    common_reqs = [good for good in card.cost if good in COMMON_GOODS]

    print(luxury_reqs, common_reqs)

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

    options = set()

    for (lux_left, lux_right), (com_left, com_right) in itertools.product(
            luxury_spread, common_spread
    ):
        options.add(
            (
                lux_left * (1 if "luxury" in player.discounts[LEFT] else 2)
                + com_left * (1 if "common" in player.discounts[LEFT] else 2),
                lux_right * (1 if "luxury" in player.discounts[RIGHT] else 2)
                + com_right * (1 if "common" in player.discounts[RIGHT] else 2),
                0,
            )
        )

    # TODO: sort and slim down options
    return list(options)
