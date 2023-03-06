from typing import Optional, List

from game.Card import Card
from game.Player import Player
from game.action.Action import Action, _get_card
from game.action.Actionable import Actionable
from util.constants import COINS


def _take_action(player: Player, card: Card, cards: List[Card]) -> None:
    player.add_token(COINS, 3)
    player.discards.append(card)
    cards.remove(card)


class DiscardAction(Action):
    def get_name(self):
        return "(d)iscard"

    def get_symbol(self) -> str:
        return "d"

    async def select_card(
        self, player: Player, cards: List[Card], arg: Optional[str]
    ) -> Optional[Actionable]:
        card = await _get_card(player, cards, arg)
        if card is None:
            return None
        player.display(f"discarding {card.name}")
        return Actionable(_take_action, [player, card, cards])


DISCARD = DiscardAction()
