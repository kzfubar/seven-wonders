import socketserver
import threading
from typing import List

from game.ServerGame import ServerGame
from game.ServerPlayer import ServerPlayer
from networking.server import WondersHandler
from networking.Config import Config
from util.util import KNOWN_IP


class WondersServer(socketserver.ThreadingTCPServer):
    players: List[ServerPlayer] = list()
    game: ServerGame

    def __init__(self):
        self.config = Config()

        self.known_ip = self.config.get(KNOWN_IP)
        self.host = self.config.get("host_ip")
        self.port = self.config.get("server_port")

        super().__init__((self.host, self.port), WondersHandler.WondersHandler)
        print("WondersServer created")

    def add_ip(self, ip: str):
        self.config.add(KNOWN_IP, ip)

    def start_game(self):
        self.game = ServerGame(self.players)
        threading.Thread(target=self.game.play).start()

    def start(self):
        print("WondersServer Started!")
        self.serve_forever()
        print("WondersServer Closed!")  # todo allow for force closing the server?
        # FIXME closing the server is broken atm, needs to be killed to close.

