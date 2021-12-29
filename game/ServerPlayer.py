from _socket import SocketType
from typing import Any

from game.Player import Player
from game.Wonder import Wonder
from messaging.MessageReceiver import MessageReceiver
from messaging.MessageSender import MessageSender
from messaging.messageTypes import MESSAGE
from messaging.messageUtil import MSG_TYPE
from util.util import min_cost


class ServerPlayer(Player):
    def __init__(self, name: str,
                 wonder: Wonder,
                 connection: SocketType):
        self.connection = connection
        self.receiver = MessageReceiver(self.connection)
        self.sender = MessageSender(self.connection)
        self.turn_over = True
        super().__init__(name, wonder)

    def display(self, message: Any):
        self.sender.send_message(message)

    def _get_input(self, message) -> str:
       pass

    def take_turn(self):
        self.turn_over = False
        self._calc_hand_costs()
        self.display(f"your hand is:\n{self._hand_to_str()}")
        self.display(f"Bury cost: {min_cost(self._get_payment_options(self.wonder.get_next_power()))}")
