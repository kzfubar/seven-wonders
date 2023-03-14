from typing import List, Optional

from game.Card import Card
from game.PaymentOption import NO_PAYMENT
from game.Player import Player
from game.action.Action import (
    Action,
    _select_payment_option,
    _get_card,
    _activate_card,
    _announce,
)
from game.action.Actionable import Actionable


def _take_action(
    player: Player, card: Card, cards: List[Card], players: List[Player]
) -> None:
    _announce(f"{player.name} used a coupon for {card}", players)
    _activate_card(player, card)
    cards.remove(card)


class CouponAction(Action):
    def get_name(self):
        return "(c)oupon"

    def get_symbol(self) -> str:
        return "c"

    async def select_card(
        self,
        player: Player,
        cards: List[Card],
        arg: Optional[str],
        players: List[Player],
    ) -> Optional[Actionable]:
        card = await _get_card(player, cards, arg)
        if card is None:
            return None
        if card.name not in player.coupons:
            player.display(f"no coupon for {card.name}!")
            return None

        player.display(f"playing {card.name} with coupon")
        successfully_played = await _select_payment_option(player, card, [NO_PAYMENT])
        player.add_card_type(card.card_type)

        return (
            Actionable(_take_action, [player, card, cards, players])
            if successfully_played
            else None
        )


COUPON = CouponAction()
