import threading
import asyncio
from typing import List
from game.Player import Player

from game.ServerGame import ServerGame
from game.ServerPlayer import ServerPlayer
from networking.server.Client import Client


class Room:
    clients: List[Client] = list()
    game: ServerGame

    def __init__(self, name: str):
        self.name = name

    def start_game(self):
        self.game = ServerGame()
        loop = asyncio.new_event_loop()
        task = loop.create_task(self.game.add_clients(self.clients))
        loop.run_until_complete(task)
        threading.Thread(target=self.game.play).start()

    def join(self, client: Client):
        self.clients.append(client)
        client.send_message(f"Joined room: {self.name}")
