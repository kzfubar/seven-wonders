from typing import List

from game.command.GameCommand import GameCommand
from networking.server.ClientConnection import ClientConnection
from util.constants import LEFT, RIGHT


class InfoCommand(GameCommand):
    name: str = "info"

    def execute(self, args: List, client: ClientConnection):
        game = self.game
        if len(args) == 0:
            player = self.game.players_by_client[client]
            client.send_message("On your left: " + player.neighbors[LEFT].short_info() + "\n")
            client.send_message("You are: " + player.short_info() + "\n")
            client.send_message("On your right: " + player.neighbors[RIGHT].short_info() + "\n")

        else:
            player_name = args[0]
            if player_name in game.players_by_name.keys():
                client.send_message(str(game.players_by_name[player_name]))
            else:
                client.send_message(
                    f"{player_name} not found. players: {game.players_by_name.keys()}"
                )
