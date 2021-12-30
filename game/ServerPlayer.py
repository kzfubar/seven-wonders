import queue
import threading
from _socket import SocketType
from typing import Any

from game.Player import Player
from game.Wonder import Wonder
from messaging.MessageReceiver import MessageReceiver
from messaging.MessageSender import MessageSender
from util.util import min_cost


class ServerPlayer(Player):
    def __init__(self, name: str,
                 wonder: Wonder,
                 connection: SocketType):
        self.connection = connection
        self.receiver = MessageReceiver(self.connection)
        self.sender = MessageSender(self.connection)
        self.message_queue: queue.Queue[str] = queue.Queue()
        self.turn_over = True
        super().__init__(name, wonder)

    def display(self, message: Any):
        self.sender.send_message(message)

    def _get_input(self, message: str) -> str:
        self.sender.send_message(message)
        return self.message_queue.get(block=True)

    def _take_turn(self):
        self.turn_over = False
        self._calc_hand_costs()
        self.display(f"your hand is:\n{self._hand_to_str()}")
        self.display(f"Bury cost: {min_cost(self._get_payment_options(self.wonder.get_next_power()))}")
        while not self.turn_over:
            player_input = list(self._get_input("(p)lay, (d)iscard or (b)ury a card: ").strip())
            action = player_input[0]
            if len(player_input) > 1:
                self.turn_over = self._take_action(action, int(player_input[1]))
            else:
                self.turn_over = self._take_action(action)

    def take_turn(self):
        threading.Thread(target=self._take_turn).start()
