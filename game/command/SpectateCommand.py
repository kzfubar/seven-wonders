from game.command.GameCommand import GameCommand
from networking.server.ClientConnection import ClientConnection


class SpectateCommand(GameCommand):
    name: str = "spectate"

    def execute(self, args: list, client: ClientConnection) -> None:  # noqa: ARG002
        self.game.spectate_clients.append(client)
