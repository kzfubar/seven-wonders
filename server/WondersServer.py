import socketserver
import threading
from typing import List

from game.ServerGame import ServerGame
from game.ServerPlayer import ServerPlayer
from server import WondersHandler


class WondersServer(socketserver.ThreadingTCPServer):
    HOST = "localhost"
    PORT = 9999
    players: List[ServerPlayer] = list()
    game: ServerGame

    def __init__(self):
        super().__init__((self.HOST, self.PORT), WondersHandler.WondersHandler)
        print("WondersServer created")

    def start_game(self):
        self.game = ServerGame(self.players)
        threading.Thread(target=self.game.play).start()

    def start(self):
        try:
            print("WondersServer Started!")
            self.serve_forever()
        except KeyboardInterrupt:
            print("WondersServer Closed!")  # todo allow for force closing the server?
            # FIXME closing the server is broken atm, needs to be killed to close.

