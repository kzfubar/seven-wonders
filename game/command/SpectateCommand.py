from typing import List

from game.command.GameCommand import GameCommand
from networking.server.ClientConnection import ClientConnection


class SpectateCommand(GameCommand):
    name: str = "spectate"

    def execute(self, args: List, client: ClientConnection):
        self.game.spectate_clients.append(client)
