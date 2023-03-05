from typing import Dict, Optional, List

from networking.server.ClientConnection import ClientConnection
from networking.server.Room import Room


class GameServer:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.room_by_client: Dict[ClientConnection, Optional[Room]] = {}

    # todo better handle if room already created
    def create_room(self, room_name: str) -> Room:
        while room_name in self.rooms:
            room_name += "*"
        room = Room(room_name)
        self.rooms[room_name] = room
        return room

    def get_room(self, room_name: str) -> Optional[Room]:
        return self.rooms[room_name]

    def handle_command(self, cmd: str, args: List, client: ClientConnection) -> bool:
        return self.room_by_client[client].handle_command(cmd, args, client)
