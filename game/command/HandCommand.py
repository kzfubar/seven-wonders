from game.command.GameCommand import GameCommand
from networking.server.ClientConnection import ClientConnection


class HandCommand(GameCommand):
    name: str = "hand"

    def execute(self, args: list, client: ClientConnection) -> None:  # noqa: ARG002
        game = self.game
        game.players_by_client[client].display_printouts()
