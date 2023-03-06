from typing import Optional, List

from game.Card import Card
from game.CostCalculator import calculate_payment_options
from game.Player import Player
from game.action.Action import Action, _select_payment_option, _get_card, _activate_card
from game.action.Actionable import Actionable


def _take_action(player: Player, card: Card, cards: List[Card]) -> None:
    _activate_card(player, card)
    cards.remove(card)


class PlayAction(Action):
    def get_name(self):
        return "(p)lay"

    def get_symbol(self) -> str:
        return "p"

    async def select_card(
        self, player: Player, cards: List[Card], arg: Optional[str]
    ) -> Optional[Actionable]:
        card = await _get_card(player, cards, arg)
        if card is None:
            return None
        payment_options = calculate_payment_options(player, card)
        player.display(f"playing {card.name}")
        successfully_played = await _select_payment_option(player, payment_options)

        return (
            Actionable(_take_action, [player, card, cards])
            if successfully_played
            else None
        )


PLAY = PlayAction()
