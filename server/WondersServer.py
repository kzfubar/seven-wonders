import socketserver
from typing import List

from game.ServerGame import ServerGame
from server import WondersHandler
from server.PlayerConnection import PlayerConnection


class WondersServer(socketserver.ThreadingTCPServer):
    HOST = "localhost"
    PORT = 9998
    connections: List[PlayerConnection] = list()
    game: ServerGame

    def __init__(self):
        super().__init__((self.HOST, self.PORT), WondersHandler.WondersHandler)
        print("WondersServer created")

    def start_game(self):
        self.game = ServerGame(self.connections)
        self.game.play()

    def start(self):
        try:
            print("WondersServer Started!")
            self.serve_forever()
        except KeyboardInterrupt:
            print("WondersServer Closed!")

