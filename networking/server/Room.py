import asyncio
from typing import List

from game.Game import Game
from networking.server.ClientConnection import ClientConnection


class Room:
    clients: List[ClientConnection] = list()
    game: Game

    def __init__(self, name: str):
        self.name = name

    async def start_game(self):
        self.game = await Game.create(self.clients)
        asyncio.create_task(self.game.play())

    def command(self, client, args):
        self.game.command(client, args)

    def join(self, client: ClientConnection):
        self.clients.append(client)
        client.send_message(f"Joined room: {self.name}")
