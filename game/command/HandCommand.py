from typing import List

from game.command.GameCommand import GameCommand
from networking.server.ClientConnection import ClientConnection


class HandCommand(GameCommand):
    name: str = "hand"

    def execute(self, args: List, client: ClientConnection):
        game = self.game
        game.players_by_client[client].display_printouts()
