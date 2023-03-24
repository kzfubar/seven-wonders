from typing import List

from game.command.GameCommand import GameCommand
from networking.server.ClientConnection import ClientConnection
from util.wonderUtils import create_wonders


class WondersCommand(GameCommand):
    name: str = "wonders"

    def execute(self, args: List, client: ClientConnection):
        for _, sides in create_wonders():
            for wonder, side in sides:
                client.send_message(wonder)
                client.send_message("\n")
