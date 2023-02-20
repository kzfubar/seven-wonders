import threading
from typing import List

from game.ServerGame import ServerGame
from networking.server.ClientConnection import ClientConnection


class Room:
    clients: List[ClientConnection] = list()

    def __init__(self, name: str):
        self.name = name

    async def start_game(self):
        game = ServerGame()
        await game.add_clients(self.clients)
        threading.Thread(target=game.play).start()

    def join(self, client: ClientConnection):
        self.clients.append(client)
        client.send_message(f"Joined room: {self.name}")
