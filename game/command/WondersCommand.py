from typing import List

from game.command.GameCommand import GameCommand
from networking.server.ClientConnection import ClientConnection
from util.wonderUtils import create_wonders


class WondersCommand(GameCommand):
    name: str = "wonders"

    def execute(self, args: List, client: ClientConnection):
        for wonder in create_wonders():
            client.send_message(wonder)
            client.send_message("\n")
