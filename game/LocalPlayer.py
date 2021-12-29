from typing import Any

from game.Player import Player
from util.util import min_cost


class LocalPlayer(Player):
    turn_over = True

    def display(self, message: Any):
        print(message)

    def _get_input(self, message) -> str:
        return input(message)

    def take_turn(self):
        self._calc_hand_costs()
        self.display(f"your hand is:\n{self._hand_to_str()}")
        self.display(f"Bury cost: {min_cost(self.wonder_payment_options)}")
        turn_over = False
        while not turn_over:
            player_input = list(input("(p)lay, (d)iscard or (b)ury a card: ").strip())
            action = player_input[0]
            if len(player_input) > 1:
                turn_over = self._take_action(action, int(player_input[1]))
            else :
                turn_over = self._take_action(action)


