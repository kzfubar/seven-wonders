from typing import List, Tuple, Optional

from game.Card import Card
from game.Player import Player
from game.action.Action import Action, _play_card, _get_card


class CouponAction(Action):
    def get_name(self):
        return "(c)oupon"

    def get_symbol(self) -> str:
        return "c"

    async def take_action(self, player: Player, arg: Optional[str]) -> bool:
        card = await _get_card(player, arg)
        if card is None:
            return False
        if card.name in player.coupons:
            player.display(f"playing {card.name} with coupon")
            successfully_played = await _play_card(player, card, [(0, 0, 0)])
            if successfully_played:
                player.hand.remove(card)
            return successfully_played
        else:
            player.display(f"no coupon for {card.name}!")


COUPON = CouponAction()
