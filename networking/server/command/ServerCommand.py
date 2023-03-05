from abc import ABC

from networking.command.Command import Command
from networking.server.GameServer import GameServer


class ServerCommand(Command, ABC):
    def __init__(self, server: GameServer):
        self.server = server
