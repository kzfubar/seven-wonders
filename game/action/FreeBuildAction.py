from game.action.Action import Action
from game.action.Actionable import Actionable
from game.Card import Card
from game.Flag import Flag
from game.PaymentOption import NO_PAYMENT
from game.Player import Player


class FreeBuildAction(Action):
    def get_name(self) -> str:
        return "(f)ree build"

    def get_symbol(self) -> str:
        return "f"

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
        player.display(f"free building {card.name}")
        successfully_played = await self._select_payment_option(
            player, card, [NO_PAYMENT]
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
        cls._announce(f"{player.name} free built {card}", players)
        cls.activate_card(player, card)
        player.flags[Flag.FREE_BUILD] = False
        cards.remove(card)


FREE_BUILD = FreeBuildAction()
