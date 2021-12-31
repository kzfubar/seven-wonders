import threading
from typing import List

from game.ServerGame import ServerGame
from game.ServerPlayer import ServerPlayer
from networking.server.Client import Client


class Room:
    clients: List[Client] = list()
    game: ServerGame

    def __init__(self, name: str):
        self.name = name

    def _get_players(self) -> List[ServerPlayer]:
        return [client.player for client in self.clients]

    def start_game(self):
        self.game = ServerGame(self._get_players())
        threading.Thread(target=self.game.play).start()

    def join(self, client: Client):
        self.clients.append(client)
        client.create_player("rhodos")
        # client.on_message("please select a wonder", client.create_player)  # todo uncomment
