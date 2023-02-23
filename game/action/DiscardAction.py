from typing import Optional, List

from game.Card import Card
from game.Player import Player
from game.action.Action import Action, _get_card


class DiscardAction(Action):
    def get_name(self):
        return "(d)iscard"

    def get_symbol(self) -> str:
        return "d"

    async def take_action(self, player: Player, cards: List[Card], arg: Optional[str]) -> bool:
        card = await _get_card(player, cards, arg)
        if card is None:
            return False
        player.display(f"discarding {card}")
        player.board["coins"] += 3
        cards.remove(card)
        player.discards.append(card)
        return True


DISCARD = DiscardAction()
