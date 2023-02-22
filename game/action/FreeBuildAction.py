from typing import Optional

from game.Flag import Flag
from game.Player import Player
from game.action.Action import Action, _play_card, _get_card


class FreeBuildAction(Action):
    def get_name(self):
        return "(f)ree build"

    def get_symbol(self) -> str:
        return "f"

    async def take_action(self, player: Player, arg: Optional[str]) -> bool:
        card = await _get_card(player, arg)
        if card is None:
            return False
        player.display(f"free building {card.name}")
        successfully_played = await _play_card(player, card, [(0, 0, 0)])
        if successfully_played:
            player.hand.remove(card)
            player.flags[Flag.FREE_BUILD] = False
        return successfully_played


FREE_BUILD = FreeBuildAction()
