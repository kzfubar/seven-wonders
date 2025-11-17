from game.command.GameCommand import GameCommand
from networking.server.ClientConnection import ClientConnection
from util.wonderUtils import create_wonders


class WondersCommand(GameCommand):
    name: str = "wonders"

    def execute(self, args: list, client: ClientConnection) -> None:  # noqa: ARG002
        for _, sides in create_wonders():
            for wonder, _side in sides:
                client.send_message(wonder)
                client.send_message("\n")
