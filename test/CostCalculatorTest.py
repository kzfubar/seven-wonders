from collections import defaultdict
from unittest import TestCase
from unittest.mock import patch

from game.CostCalculator import calculate_payment_options
from game.Card import Card, Effect
from game.Player import Player
from game.Resource import Resource
from game.Side import Side
from game.Wonder import Wonder
from util.cardUtils import get_all_cards
from util.constants import COMMON, LEFT, RIGHT


class CostCalculatorTest(TestCase):
    ALL_CARDS = get_all_cards(7)
    victim: Player
    left: Player
    right: Player

    @patch("networking.server.ClientConnection")
    def setUp(self, connection) -> None:
        self.victim = Player(Wonder("", "", Side("A"), "", []), connection)
        self.left = Player(Wonder("", "", Side("A"), "", []), connection)
        self.right = Player(Wonder("", "", Side("A"), "", []), connection)

        self.victim.neighbors[LEFT] = self.left
        self.victim.neighbors[RIGHT] = self.right

    def test_caravansery_not_playable_when_no_production(self):
        caravansery = self._get_card("Caravansery")

        cost = calculate_payment_options(self.victim, caravansery)
        self.assertFalse(cost)

    def test_caravansery_playable_when_self_production(self):
        caravansery = self._get_card("Caravansery")

        self.victim.effects["produce"].append(
            Effect("produce", [Resource("w", 2)], [], ["self"], COMMON)
        )
        one_production_cost = calculate_payment_options(self.victim, caravansery)
        self.assertTrue(one_production_cost)

        self._clear_effects()

        self.victim.effects["produce"].append(
            Effect("produce", [Resource("w", 1)], [], ["self"], COMMON)
        )
        self.victim.effects["produce"].append(
            Effect("produce", [Resource("w", 1)], [], ["self"], COMMON)
        )
        multiple_production_cost = calculate_payment_options(self.victim, caravansery)
        self.assertTrue(multiple_production_cost)

        self._clear_effects()

        self.victim.effects["produce"].append(
            Effect(
                "produce", [Resource("w", 1), Resource("b", 1)], [], ["self"], COMMON
            )
        )
        self.victim.effects["produce"].append(
            Effect("produce", [Resource("w", 1)], [], ["self"], COMMON)
        )
        optional_production_cost = calculate_payment_options(self.victim, caravansery)
        self.assertTrue(optional_production_cost)

    def test_caravansery_playable_when_neighbors_production(self):
        caravansery = self._get_card("Caravansery")

        self.left.effects["produce"].append(
            Effect("produce", [Resource("w", 2)], [], ["self"], COMMON)
        )
        left_cost = calculate_payment_options(self.victim, caravansery)
        self.assertTrue(left_cost)
        self.assertEqual(left_cost[0].total(), 4)

        self._clear_effects()

        self.right.effects["produce"].append(
            Effect("produce", [Resource("w", 2)], [], ["self"], COMMON)
        )
        right_cost = calculate_payment_options(self.victim, caravansery)
        self.assertTrue(right_cost)
        self.assertEqual(right_cost[0].total(), 4)

    def test_caravansery_playable_when_shared_production(self):
        caravansery = self._get_card("Caravansery")

        self.victim.effects["produce"].append(
            Effect("produce", [Resource("w", 1)], [], ["self"], COMMON)
        )
        self.left.effects["produce"].append(
            Effect("produce", [Resource("w", 1)], [], ["self"], COMMON)
        )
        shared_left_cost = calculate_payment_options(self.victim, caravansery)
        self.assertTrue(shared_left_cost)

        self._clear_effects()

        self.victim.effects["produce"].append(
            Effect("produce", [Resource("w", 1)], [], ["self"], COMMON)
        )
        self.right.effects["produce"].append(
            Effect("produce", [Resource("w", 1)], [], ["self"], COMMON)
        )
        shared_right_cost = calculate_payment_options(self.victim, caravansery)
        self.assertTrue(shared_right_cost)

    def _get_card(self, card_name: str) -> Card:
        for card in self.ALL_CARDS:
            if card.name == card_name:
                return card
        raise KeyError

    def _clear_effects(self) -> None:
        self.victim.effects = defaultdict(list)
        self.left.effects = defaultdict(list)
        self.right.effects = defaultdict(list)
