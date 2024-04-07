from networking.server.ClientConnection import ClientConnection
from networking.server.command.ServerCommand import ServerCommand


class LeaveCommand(ServerCommand):
    name: str = "leave"

    def execute(self, args: str, client: ClientConnection):
        if (
            client not in self.server.room_by_client
            or self.server.room_by_client[client] is None
        ):
            client.send_message("You are not in a room")
            return
        room = self.server.room_by_client[client]
        self.server.leave_room(client)
        client.send_message(f"You have left {room.name}")
