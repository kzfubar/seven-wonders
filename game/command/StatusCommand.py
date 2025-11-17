from game.command.GameCommand import GameCommand
from networking.server.ClientConnection import ClientConnection


class StatusCommand(GameCommand):
    name: str = "status"

    def execute(self, args: list, client: ClientConnection) -> None:  # noqa: ARG002
        if not self.game.running:
            client.send_message("Game has not started")
            return
        for player in self.game.players:
            client.send_message(f"{player.name} {player.status}")
