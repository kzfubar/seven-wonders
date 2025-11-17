from networking.server.ClientConnection import ClientConnection
from networking.server.Room import Room


class GameServer:
    def __init__(self) -> None:
        self.room_by_name: dict[str, Room] = {}
        self.room_by_client: dict[ClientConnection, Room | None] = {}

    def cleanup(self, client: ClientConnection) -> None:
        self.leave_room(client)

    def leave_room(self, client: ClientConnection) -> None:
        if client not in self.room_by_client:
            return
        client_room = self.room_by_client[client]
        if client_room is not None:
            client_room.leave(client)
            if client_room.size() == 0:
                del self.room_by_name[client_room.name]
            del self.room_by_client[client]

    # todo better handle if room already created
    def create_room(self, room_name: str) -> Room:
        while room_name in self.room_by_name:
            room_name += "*"
        room = Room(room_name)
        self.room_by_name[room_name] = room
        return room

    def get_room(self, room_name: str) -> Room:
        return self.room_by_name[room_name]

    def handle_command(self, cmd: str, args: list, client: ClientConnection) -> bool:
        room = self.room_by_client.get(client)
        if room is None:
            return False
        return room.handle_command(cmd, args, client)
