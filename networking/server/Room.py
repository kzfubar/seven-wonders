import asyncio
from typing import List, Dict

from game.Game import Game
from game.command.ToggleCommand import ToggleCommand
from game.command.HandCommand import HandCommand
from game.command.InfoCommand import InfoCommand
from game.command.TellCommand import TellCommand
from game.command.WondersCommand import WondersCommand
from networking.server.command.Command import Command
from networking.server.ClientConnection import ClientConnection


def _game_commands(game: Game) -> Dict[str, Command]:
    commands = [
        InfoCommand(game),
        TellCommand(game),
        WondersCommand(game),
        HandCommand(game),
        ToggleCommand(game),
    ]
    return {cmd.name: cmd for cmd in commands}


class Room:
    def __init__(self, name: str):
        self.name: str = name
        self.game: Game = Game()
        self.commands: Dict[str, Command] = _game_commands(self.game)
        self.clients: List[ClientConnection] = list()

    def start_game(self) -> bool:
        if self.game.running:
            return False
        asyncio.create_task(self._start_game())
        return True

    async def _start_game(self):
        await self.game.start(self.clients)
        for client in self.clients:
            client.send_message("game is over.")

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
