from game.command.GameCommand import GameCommand
from networking.server.ClientConnection import ClientConnection


class InfoCommand(GameCommand):
    name: str = "info"

    def execute(self, args: str, client: ClientConnection):
        game = self.game
        player_name = args[0]
        if player_name in game.players_by_name.keys():
            client.send_message(str(game.players_by_name[player_name]))
        else:
            client.send_message(
                f"{player_name} not found. players: {game.players_by_name.keys()}"
            )
