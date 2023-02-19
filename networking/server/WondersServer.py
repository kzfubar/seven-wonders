import socketserver
from _socket import SocketType
from typing import Dict, Optional

from networking.server import WondersHandler
from networking.Config import Config
from networking.server.Room import Room
from util.util import KNOWN_IP


class WondersServer(socketserver.ThreadingTCPServer):
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.clients: Dict[str, Optional[Room]] = {}

        self.config = Config()
        self.known_ip = self.config.get(KNOWN_IP)
        self.host = self.config.get("host_ip")
        self.port = self.config.get("server_port")

        super().__init__((self.host, self.port), WondersHandler.WondersHandler)
        print("WondersServer created")

    def add_ip(self, ip: str):
        self.config.add(KNOWN_IP, ip)

    def create_room(
        self, room_name: str
    ) -> Room:  # todo better handle if room already created
        while room_name in self.rooms:
            room_name += "*"
        room = Room(room_name)
        self.rooms[room_name] = room
        return room

    def get_room(self, room_name: str) -> Optional[Room]:
        return self.rooms[room_name]

    # todo def get_room_names()

    def start(self):
        print("WondersServer Started!")
        self.serve_forever()
        print("WondersServer Closed!")  # todo allow for force closing the server?
        # FIXME closing the server is broken atm, needs to be killed to close.
