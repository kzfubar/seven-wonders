import asyncio
from typing import List, Dict

from game.Game import Game
from game.command.InfoCommand import InfoCommand
from networking.server.command.Command import Command
from networking.server.ClientConnection import ClientConnection


def _game_commands(game: Game) -> Dict[str, Command]:
    commands = [InfoCommand(game)]
    return {cmd.name: cmd for cmd in commands}


class Room:
    def __init__(self, name: str):
        self.name: str = name
        self.game: Game = Game()
        self.commands: Dict[str, Command] = _game_commands(self.game)
        self.clients: List[ClientConnection] = list()

    async def start_game(self):
        asyncio.create_task(self.game.start(self.clients))

    def handle_command(self, cmd: str, args: List, client: ClientConnection) -> bool:
        if cmd in self.commands:
            self.commands[cmd].execute(args, client)
            return True
        else:
            return False

    def join(self, client: ClientConnection):
        self.clients.append(client)
        client.send_message(f"Joined room: {self.name}")
        client.send_message(f"Currently in room: {[c.name for c in self.clients]}")
        for c in self.clients:
            c.send_message(f"{client.name} has joined the room")
