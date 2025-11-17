from networking.server.ClientConnection import ClientConnection
from networking.server.command.ServerCommand import ServerCommand


class StartCommand(ServerCommand):
    name: str = "start"

    def execute(self, args: list[str], client: ClientConnection) -> None:  # noqa: ARG002
        room = self.server.room_by_client.get(client)
        if room is not None and not room.start_game():
            client.send_message("Game already running!")
