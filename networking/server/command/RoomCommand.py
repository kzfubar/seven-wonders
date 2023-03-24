from networking.server.ClientConnection import ClientConnection
from networking.server.command.ServerCommand import ServerCommand


class RoomCommand(ServerCommand):
    name: str = "room"

    def execute(self, args: str, client: ClientConnection):
        self.server.leave_room(client)
        room_name = args[0]
        if room_name not in self.server.room_by_name:
            self.server.create_room(room_name)
        room = self.server.get_room(room_name)
        room.join(client)
        self.server.room_by_client[client] = room
