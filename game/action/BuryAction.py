from typing import Optional, List

from game.Card import Card
from game.CostCalculator import calculate_payment_options
from game.Player import Player
from game.action.Action import Action, _play_card, _get_card


class BuryAction(Action):
    def get_name(self):
        return "(b)ury"

    def get_symbol(self) -> str:
        return "b"

    async def take_action(self, player: Player, cards: List[Card], arg: Optional[str]) -> bool:
        card = await _get_card(player, cards, arg)
        if card is None:
            return False
        player.display(f"burying {card.name}")
        wonder_power = player.wonder.get_next_power()
        payment_options = calculate_payment_options(player, card)
        successfully_played = await _play_card(player, wonder_power, payment_options)
        if successfully_played:
            player.wonder.increment_level()
            cards.remove(card)
        return successfully_played


BURY = BuryAction()
