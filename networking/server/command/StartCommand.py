from networking.server.ClientConnection import ClientConnection
from networking.server.command.ServerCommand import ServerCommand


class StartCommand(ServerCommand):
    name: str = "start"

    def execute(self, args: str, client: ClientConnection):
        room = self.server.room_by_client.get(client)
        if room is not None:
            if not room.start_game():
                client.send_message("Game already running!")
