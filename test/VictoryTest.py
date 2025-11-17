from unittest import TestCase
from unittest.mock import patch

from game.Card import Card, Effect
from game.Player import Player
from game.Resource import Resource
from game.Side import Side
from game.VictoryCalculator import VictoryCalculator
from game.Wonder import Wonder
from networking.server.ClientConnection import ClientConnection
from util.cardUtils import get_all_cards
from util.constants import SCIENCE, WONDER_POWER


class VictoryPointsTest(TestCase):
    ALL_CARDS = get_all_cards(7)
    victim: Player
    left: Player
    right: Player

    victory_calculator = VictoryCalculator(ALL_CARDS)

    @patch("networking.server.ClientConnection")
    def test_points_from_three_science(self, connection: ClientConnection) -> None:
        self.victim = Player(
            Wonder(
                "wood_wonder", "", Side("A"), Card("", "", 0, WONDER_POWER, [], []), []
            ),
            connection,
        )
        self.victim.effects["research"].append(
            Effect("research", [Resource("x", 1)], [], ["self"], SCIENCE)
        )
        self.victim.effects["research"].append(
            Effect("research", [Resource("y", 1)], [], ["self"], SCIENCE)
        )
        self.victim.effects["research"].append(
            Effect("research", [Resource("z", 1)], [], ["self"], SCIENCE)
        )

        vp = self.victory_calculator.get_victory(self.victim)

        assert vp["science"] == 10

    @patch("networking.server.ClientConnection")
    def test_points_from_three_science_one_choice(
        self, connection: ClientConnection
    ) -> None:
        self.victim = Player(
            Wonder(
                "wood_wonder", "", Side("A"), Card("", "", 0, WONDER_POWER, [], []), []
            ),
            connection,
        )
        self.victim.effects["research"].append(
            Effect("research", [Resource("x", 1)], [], ["self"], SCIENCE)
        )
        self.victim.effects["research"].append(
            Effect("research", [Resource("y", 1)], [], ["self"], SCIENCE)
        )
        self.victim.effects["research"].append(
            Effect(
                "research",
                [Resource("x", 1), Resource("y", 1), Resource("z", 1)],
                [],
                ["self"],
                SCIENCE,
            )
        )

        vp = self.victory_calculator.get_victory(self.victim)

        assert vp["science"] == 10

    @patch("networking.server.ClientConnection")
    def test_points_four_science_choices(self, connection: ClientConnection) -> None:
        self.victim = Player(
            Wonder(
                "wood_wonder", "", Side("A"), Card("", "", 0, WONDER_POWER, [], []), []
            ),
            connection,
        )
        self.victim.effects["research"].append(
            Effect(
                "research",
                [Resource("x", 1), Resource("y", 1), Resource("z", 1)],
                [],
                ["self"],
                SCIENCE,
            )
        )
        self.victim.effects["research"].append(
            Effect(
                "research",
                [Resource("x", 1), Resource("y", 1), Resource("z", 1)],
                [],
                ["self"],
                SCIENCE,
            )
        )

        self.victim.effects["research"].append(
            Effect(
                "research",
                [Resource("x", 1), Resource("y", 1), Resource("z", 1)],
                [],
                ["self"],
                SCIENCE,
            )
        )
        self.victim.effects["research"].append(
            Effect(
                "research",
                [Resource("x", 1), Resource("y", 1), Resource("z", 1)],
                [],
                ["self"],
                SCIENCE,
            )
        )

        vp = self.victory_calculator.get_victory(self.victim)

        assert vp["science"] == 16

    @patch("networking.server.ClientConnection")
    def test_points_ten_science_choices(self, connection: ClientConnection) -> None:
        self.victim = Player(
            Wonder(
                "wood_wonder", "", Side("A"), Card("", "", 0, WONDER_POWER, [], []), []
            ),
            connection,
        )
        for _ in range(10):
            self.victim.effects["research"].append(
                Effect(
                    "research",
                    [Resource("x", 1), Resource("y", 1), Resource("z", 1)],
                    [],
                    ["self"],
                    SCIENCE,
                )
            )

        vp = self.victory_calculator.get_victory(self.victim)

        assert vp["science"] == 100
