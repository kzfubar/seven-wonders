import random

from bot.BasePlayer import BasePlayer


class RandomPlayer(BasePlayer):
    def _handle_input(self, data: dict) -> str:
        return random.choice(data["options"]) + str(
            random.randrange(0, len(self.game_state["self"]["hand"]))
        )

    def _handle_payment(self, data: dict) -> str:
        return random.choice(data["options"])
