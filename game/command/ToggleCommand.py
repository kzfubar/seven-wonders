from game.command.GameCommand import GameCommand
from networking.server.ClientConnection import ClientConnection


class ToggleCommand(GameCommand):
    name: str = "toggle"

    def execute(self, args: list, client: ClientConnection) -> None:
        toggle = args[0]
        try:
            value = args[1].lower() == "true"
            self.game.players_by_client[client].toggles[toggle] = value
            client.send_message(f"set {toggle} to {value}")
        except KeyError:
            client.send_message(f"failed to set {toggle}")
