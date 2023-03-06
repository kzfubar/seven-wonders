from typing import Optional, List

from game.Card import Card
from game.Player import Player
from game.action.Action import Action, _get_card, _announce
from game.action.Actionable import Actionable
from util.constants import COINS


def _take_action(player: Player, card: Card, cards: List[Card], players: List[Player]) -> None:
    _announce(f"{player.name} discarded a card for 3 coins", players)
    player.add_token(COINS, 3)
    player.discards.append(card)
    cards.remove(card)


class DiscardAction(Action):
    def get_name(self):
        return "(d)iscard"

    def get_symbol(self) -> str:
        return "d"

    async def select_card(
        self, player: Player, cards: List[Card], arg: Optional[str], players: List[Player]
    ) -> Optional[Actionable]:
        card = await _get_card(player, cards, arg)
        if card is None:
            return None
        player.display(f"discarding {card.name}")
        return Actionable(_take_action, [player, card, cards, players])


DISCARD = DiscardAction()
