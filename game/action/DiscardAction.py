from game.action.Action import Action
from game.action.Actionable import Actionable
from game.Card import Card
from game.Player import Player
from util.constants import COINS


class DiscardAction(Action):
    def get_name(self) -> str:
        return "(d)iscard"

    def get_symbol(self) -> str:
        return "d"

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
        player.display(f"discarding {card.name}")
        return Actionable(self._take_action, [player, card, cards, players])

    @classmethod
    def _take_action(
        cls, player: Player, card: Card, cards: list[Card], players: list[Player]
    ) -> None:
        cls._announce(f"{player.name} discarded a card for 3 coins", players)
        player.add_token(COINS, 3)
        player.discards.append(card)
        cards.remove(card)


DISCARD = DiscardAction()
