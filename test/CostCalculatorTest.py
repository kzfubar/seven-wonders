from collections import defaultdict
from unittest import TestCase
from unittest.mock import patch

from game import CostCalculator
from game.Card import Card, Effect
from game.Player import Player
from game.Wonder import Wonder
from util.cardUtils import get_all_cards
from util.constants import LEFT, RIGHT


class CostCalculatorTest(TestCase):
    ALL_CARDS = get_all_cards(7)
    victim: Player
    left: Player
    right: Player

    @patch('networking.server.ClientConnection')
    def setUp(self, connection) -> None:
        self.victim = Player(Wonder("", "", []), connection)
        self.left = Player(Wonder("", "", []), connection)
        self.right = Player(Wonder("", "", []), connection)

        self.victim.neighbors[LEFT] = self.left
        self.victim.neighbors[RIGHT] = self.right

    def test_caravansery_not_playable_when_no_production(self):
        caravansery = self._get_card("Caravansery")

        cost = CostCalculator.calculate_payment_options(self.victim, caravansery)
        self.assertFalse(cost)

    def test_caravansery_playable_when_self_production(self):
        caravansery = self._get_card("Caravansery")

        self.victim.effects["produce"].append(Effect("produce", [("w", 2)], [], ["self"], "common"))
        one_production_cost = CostCalculator.calculate_payment_options(self.victim, caravansery)
        self.assertTrue(one_production_cost)

        self._clear_effects()

        self.victim.effects["produce"].append(Effect("produce", [("w", 1)], [], ["self"], "common"))
        self.victim.effects["produce"].append(Effect("produce", [("w", 1)], [], ["self"], "common"))
        multiple_production_cost = CostCalculator.calculate_payment_options(self.victim, caravansery)
        self.assertTrue(multiple_production_cost)

        self._clear_effects()

        self.victim.effects["produce"].append(Effect("produce", [("w", 1), ("b", 1)], [], ["self"], "common"))
        self.victim.effects["produce"].append(Effect("produce", [("w", 1)], [], ["self"], "common"))
        optional_production_cost = CostCalculator.calculate_payment_options(self.victim, caravansery)
        self.assertTrue(optional_production_cost)

    def test_caravansery_playable_when_neighbhors_production(self):
        caravansery = self._get_card("Caravansery")

        self.left.effects["produce"].append(Effect("produce", [("w", 2)], [], ["self"], "common"))
        left_cost = CostCalculator.calculate_payment_options(self.victim, caravansery)
        self.assertTrue(left_cost)

        self._clear_effects()

        self.right.effects["produce"].append(Effect("produce", [("w", 2)], [], ["self"], "common"))
        right_cost = CostCalculator.calculate_payment_options(self.victim, caravansery)
        self.assertTrue(right_cost)

    def test_caravansery_playable_when_shared_production(self):
        caravansery = self._get_card("Caravansery")

        self.victim.effects["produce"].append(Effect("produce", [("w", 1)], [], ["self"], "common"))
        self.left.effects["produce"].append(Effect("produce", [("w", 1)], [], ["self"], "common"))
        shared_left_cost = CostCalculator.calculate_payment_options(self.victim, caravansery)
        self.assertTrue(shared_left_cost)

        self._clear_effects()

        self.victim.effects["produce"].append(Effect("produce", [("w", 1)], [], ["self"], "common"))
        self.right.effects["produce"].append(Effect("produce", [("w", 1)], [], ["self"], "common"))
        shared_right_cost = CostCalculator.calculate_payment_options(self.victim, caravansery)
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