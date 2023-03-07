from unittest import TestCase
from unittest.mock import patch

from game.Card import Effect
from game.Player import Player
from game.Wonder import Wonder
from util.cardUtils import get_all_cards
from util.constants import SCIENCE


class VictoryPointsTest(TestCase):
    ALL_CARDS = get_all_cards(7)
    victim: Player
    left: Player
    right: Player

    @patch("networking.server.ClientConnection")
    def test_points_from_three_science(self, connection):

        self.victim = Player(Wonder("wood_wonder", "w", []), connection)
        self.victim.effects["research"].append(
            Effect("research", [("x", 1)], [], ["self"], SCIENCE)
        )
        self.victim.effects["research"].append(
            Effect("research", [("y", 1)], [], ["self"], SCIENCE)
        )
        self.victim.effects["research"].append(
            Effect("research", [("z", 1)], [], ["self"], SCIENCE)
        )

        vp = self.victim.get_victory()

        self.assertEqual(vp["science"], 10)

    @patch("networking.server.ClientConnection")
    def test_points_from_three_science_one_choice(self, connection):

        self.victim = Player(Wonder("wood_wonder", "w", []), connection)
        self.victim.effects["research"].append(
            Effect("research", [("x", 1)], [], ["self"], SCIENCE)
        )
        self.victim.effects["research"].append(
            Effect("research", [("y", 1)], [], ["self"], SCIENCE)
        )
        self.victim.effects["research"].append(
            Effect("research", [("x", 1), ("y", 1), ("z", 1)], [], ["self"], SCIENCE)
        )

        vp = self.victim.get_victory()

        self.assertEqual(vp["science"], 10)

    @patch("networking.server.ClientConnection")
    def test_points_four_science_choices(self, connection):

        self.victim = Player(Wonder("wood_wonder", "w", []), connection)
        self.victim.effects["research"].append(
            Effect("research", [("x", 1), ("y", 1), ("z", 1)], [], ["self"], SCIENCE)
        )
        self.victim.effects["research"].append(
            Effect("research", [("x", 1), ("y", 1), ("z", 1)], [], ["self"], SCIENCE)
        )

        self.victim.effects["research"].append(
            Effect("research", [("x", 1), ("y", 1), ("z", 1)], [], ["self"], SCIENCE)
        )
        self.victim.effects["research"].append(
            Effect("research", [("x", 1), ("y", 1), ("z", 1)], [], ["self"], SCIENCE)
        )

        vp = self.victim.get_victory()

        self.assertEqual(vp["science"], 16)

    @patch("networking.server.ClientConnection")
    def test_points_ten_science_choices(self, connection):

        self.victim = Player(Wonder("wood_wonder", "w", []), connection)
        for _ in range(10):
            self.victim.effects["research"].append(
                Effect(
                    "research", [("x", 1), ("y", 1), ("z", 1)], [], ["self"], SCIENCE
                )
            )

        vp = self.victim.get_victory()

        self.assertEqual(vp["science"], 100)
