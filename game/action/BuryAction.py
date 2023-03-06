from typing import Optional, List

from game.Card import Card
from game.CostCalculator import calculate_payment_options
from game.Player import Player
from game.action.Action import Action, _select_payment_option, _get_card, _activate_card, _announce
from game.action.Actionable import Actionable


def _take_action(
    player: Player, wonder_card: Card, card: Card, cards: List[Card], players: List[Player]
) -> None:
    _announce(f"{player.name} buried a card", players)
    _activate_card(player, wonder_card)
    player.wonder.increment_level()
    cards.remove(card)


class BuryAction(Action):
    def get_name(self):
        return "(b)ury"

    def get_symbol(self) -> str:
        return "b"

    async def select_card(
        self, player: Player, cards: List[Card], arg: Optional[str], players: List[Player]
    ) -> Optional[Actionable]:
        card = await _get_card(player, cards, arg)
        if card is None:
            return None
        player.display(f"burying {card.name}")
        wonder_power = player.wonder.get_next_power()
        payment_options = calculate_payment_options(player, wonder_power)
        successfully_played = await _select_payment_option(player, payment_options)

        return (
            Actionable(_take_action, [player, wonder_power, card, cards, players])
            if successfully_played
            else None
        )


BURY = BuryAction()
