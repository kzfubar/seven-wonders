from typing import List

from game.command.GameCommand import GameCommand
from networking.server.ClientConnection import ClientConnection


class TellCommand(GameCommand):
    name: str = "tell"

    def execute(self, args: List, client: ClientConnection):
        player_name = args.pop(0)
        msg = ' '.join(args)
        messenger = self.game.players_by_client[client]
        if player_name in self.game.players_by_name.keys():
            self.game.players_by_name[player_name].display(f"{messenger}: {msg}")
        else:
            client.send_message(f"{player_name} not found. players: {self.game.players_by_name.keys()}")
