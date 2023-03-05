import asyncio

from networking.server.ClientConnection import ClientConnection
from networking.server.command.ServerCommand import ServerCommand


class StartCommand(ServerCommand):
    name: str = "start"

    def execute(self, args: str, client: ClientConnection):
        room = self.server.room_by_client.get(client)
        if room is not None:
            asyncio.create_task(room.start_game())  # todo handle not enough players gracefully
            print("starting game")
