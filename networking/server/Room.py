import asyncio
from typing import List

from game.Game import Game
from networking.server.ClientConnection import ClientConnection


class Room:
    clients: List[ClientConnection] = list()

    def __init__(self, name: str):
        self.name = name

    async def start_game(self):
        game = Game()
        await game.add_clients(self.clients)
        asyncio.create_task(game.play())

    def join(self, client: ClientConnection):
        self.clients.append(client)
        client.send_message(f"Joined room: {self.name}")
