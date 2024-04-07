import random

from bot.GamePlayer import GamePlayer


class RandomPlayer(GamePlayer):
    def _handle_input(self, data: dict) -> str:
        return random.choice(data["options"]) + str(
            random.randrange(0, len(self.game_state["hand"]))
        )

    def _handle_payment(self, data: dict) -> str:
        return random.choice(data["options"])
