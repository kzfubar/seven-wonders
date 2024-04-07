from unittest import TestCase
from unittest.mock import patch

from game.Card import Card, Effect
from game.CostCalculator import calculate_payment_options
from game.Player import Player
from game.Resource import Resource
from game.Side import Side
from game.Wonder import Wonder
from game.action import Action
from util.cardUtils import get_all_cards
from util.constants import COMMON, LEFT, RIGHT, WONDER_POWER


class ResourcePurchaseTest(TestCase):
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

    @patch("networking.server.ClientConnection")
    def test_playable_when_self_wonder_production(self, connection):
        caravansery = self._get_card("Caravansery")

        self.victim = Player(
            Wonder(
                "wood_wonder",
                "",
                Side("A"),
                Card(
                    "",
                    "",
                    0,
                    WONDER_POWER,
                    [],
                    [Effect("produce", [Resource("w", 2)], [], ["self"], COMMON)],
                ),
                [],
            ),
            connection,
        )
        self.victim.neighbors[LEFT] = self.left
        self.victim.neighbors[RIGHT] = self.right
        # print(self.victim)

        self.victim.effects["produce"].append(
            Effect("produce", [Resource("w", 1)], [], ["self"], COMMON)
        )
        Action.activate_card(self.victim, self.victim.wonder.power)
        cost = calculate_payment_options(self.victim, caravansery)
        self.assertTrue(cost)

    @patch("networking.server.ClientConnection")
    def test_not_playable_when_neighbor_wonder_production(self, connection):
        caravansery = self._get_card("Caravansery")

        self.left = Player(Wonder("wood_wonder", "", Side("A"), "w", []), connection)
        self.victim.neighbors[LEFT] = self.left
        self.victim.effects["produce"].append(
            Effect("produce", [Resource("w", 1)], [], ["self"], COMMON)
        )
        cost = calculate_payment_options(self.victim, caravansery)
        self.assertFalse(cost)

    def _get_card(self, card_name: str) -> Card:
        for card in self.ALL_CARDS:
            if card.name == card_name:
                return card
        raise KeyError
