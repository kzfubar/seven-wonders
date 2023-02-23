from typing import Optional, List

from game.Card import Card
from game.CostCalculator import calculate_payment_options
from game.Player import Player
from game.action.Action import Action, _play_card, _get_card


class PlayAction(Action):
    def get_name(self):
        return "(p)lay"

    def get_symbol(self) -> str:
        return "p"

    async def take_action(self, player: Player, cards: List[Card], arg: Optional[str]) -> bool:
        card = await _get_card(player, cards, arg)
        if card is None:
            return False
        payment_options = calculate_payment_options(player, card)
        player.display(f"playing {card.name}")
        successfully_played = await _play_card(player, card, payment_options)
        if successfully_played:
            cards.remove(card)
        return successfully_played


PLAY = PlayAction()
