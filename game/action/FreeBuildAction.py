from typing import Optional, List

from game.Card import Card
from game.Flag import Flag
from game.Player import Player
from game.action.Action import Action, _select_payment_option, _get_card, _activate_card
from game.action.Actionable import Actionable


def _take_action(player: Player, card: Card, cards: List[Card]) -> None:
    _activate_card(player, card)
    player.flags[Flag.FREE_BUILD] = False
    cards.remove(card)


class FreeBuildAction(Action):
    def get_name(self):
        return "(f)ree build"

    def get_symbol(self) -> str:
        return "f"

    async def select_card(
        self, player: Player, cards: List[Card], arg: Optional[str]
    ) -> Optional[Actionable]:
        card = await _get_card(player, cards, arg)
        if card is None:
            return None
        player.display(f"free building {card.name}")
        successfully_played = await _select_payment_option(player, [(0, 0, 0)])
        player.board[card.card_type] += 1

        return (
            Actionable(_take_action, [player, card, cards])
            if successfully_played
            else None
        )


FREE_BUILD = FreeBuildAction()
