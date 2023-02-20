import asyncio
from typing import List

from game.Game import Game
from game.ServerPlayer import ServerPlayer
from networking.server.ClientConnection import ClientConnection
from util.wonderUtils import ALL_WONDERS, get_wonder


class ServerGame(Game):
    players: List[ServerPlayer]

    def __init__(self):
        pass

    async def add_clients(self, clients: List[ClientConnection]):
        num_players = len(clients)
        if num_players < 3:
            raise Exception(f"min players is 3, cannot start the game with {num_players}")
            # todo make this actually message the player with error
        if num_players > len(ALL_WONDERS):
            raise Exception(f"more players than wonders, cannot start the game with {num_players}")
        self.players = []
        await asyncio.gather(*(self._create_player(client) for client in clients))
        self._message_players(f"creating game with {num_players}...")

    async def _create_player(self, client: ClientConnection) -> None:
        wonder_name = ""
        client.send_message("Enter your wonder")
        while wonder_name == "":
            msg = await client.get_message()

            if msg not in [wonder.name for wonder in ALL_WONDERS]:
                client.send_message("Invalid wonder name")

            elif msg in (player.wonder for player in self.players):
                client.send_message("Wonder in use")

            else:
                wonder_name = msg
        wonder = get_wonder(wonder_name)
        self.players.append(ServerPlayer(client.name, wonder, client))

    def _message_players(self, message: str):
        for player in self.players:
            player.display(message)

    def _round_over(self) -> bool:
        for player in self.players:
            if not player.turn_over:
                return False
        return True

    def _play_round(self):
        for player_number, player in enumerate(self.players):
            player.display(f"{player.name}, take your turn")
            player.take_turn()
            player.display(player.effects)
        while not self._round_over():
            continue
