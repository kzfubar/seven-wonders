from game.action.Action import Action
from game.action.Actionable import Actionable
from game.Card import Card
from game.CostCalculator import calculate_payment_options
from game.Player import Player


class PlayAction(Action):
    def get_name(self) -> str:
        return "(p)lay"

    def get_symbol(self) -> str:
        return "p"

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
        payment_options = calculate_payment_options(player, card)
        player.display(f"playing {card.name}")
        successfully_played = await self._select_payment_option(
            player, card, payment_options
        )

        return (
            Actionable(self._take_action, [player, card, cards, players])
            if successfully_played
            else None
        )

    @classmethod
    def _take_action(
        cls, player: Player, card: Card, cards: list[Card], players: list[Player]
    ) -> None:
        cls._announce(f"{player.name} played {card}", players)
        cls.activate_card(player, card)
        cards.remove(card)


PLAY = PlayAction()
