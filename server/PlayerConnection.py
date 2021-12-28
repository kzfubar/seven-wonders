from socket import SocketType

from Player import Player


class PlayerConnection:
    def __init__(self, player: Player, connection: SocketType):
        self.player = player
        self.connection = connection
