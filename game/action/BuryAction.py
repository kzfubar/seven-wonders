from game.action.Action import (
    Action,
)
from game.action.Actionable import Actionable
from game.Card import Card
from game.CostCalculator import calculate_payment_options
from game.Player import Player


class BuryAction(Action):
    def get_name(self) -> str:
        return "(b)ury"

    def get_symbol(self) -> str:
        return "b"

    async def select_card(
        self,
        player: Player,
        cards: list[Card],
        arg: str | None,
        players: list[Player],
    ) -> Actionable | None:
        card = await self._get_card(player, cards, arg)
        if card is None:
            return None
        player.display(f"burying {card.name}")
        wonder_stage = player.wonder.get_next_stage()
        payment_options = calculate_payment_options(player, wonder_stage)
        successfully_played = await self._select_payment_option(
            player, wonder_stage, payment_options
        )

        return (
            Actionable(self._take_action, [player, wonder_stage, card, cards, players])
            if successfully_played
            else None
        )

    @classmethod
    def _take_action(
        cls,
        player: Player,
        wonder_card: Card,
        card: Card,
        cards: list[Card],
        players: list[Player],
    ) -> None:
        cls._announce(f"{player.name} buried a card", players)
        cls.activate_card(player, wonder_card)
        player.wonder.increment_level()
        cards.remove(card)


BURY = BuryAction()
