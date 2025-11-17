from game.command.GameCommand import GameCommand
from networking.server.ClientConnection import ClientConnection


class TellCommand(GameCommand):
    name: str = "tell"

    def execute(self, args: list, client: ClientConnection) -> None:
        player_name = args.pop(0)
        msg = " ".join(args)
        messenger = self.game.players_by_client[client].name
        if player_name in self.game.players_by_name:
            self.game.players_by_name[player_name].display(f"{messenger}: {msg}")
        else:
            client.send_message(
                f"{player_name} not found. players: {self.game.players_by_name.keys()}"
            )
