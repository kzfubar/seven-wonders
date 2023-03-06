from game.command.GameCommand import GameCommand
from networking.server.ClientConnection import ClientConnection


class TellCommand(GameCommand):
    name: str = "tell"

    def execute(self, args: str, client: ClientConnection):
        player_name = args[0]
        msg = args[1]
        if player_name in self.game.players_by_name.keys():
            self.game.players_by_name[player_name].display(msg)
        else:
            client.send_message(f"{player_name} not found. players: {self.game.players_by_name.keys()}")
