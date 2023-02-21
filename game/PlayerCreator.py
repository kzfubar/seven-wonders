import asyncio
from typing import List

from game.Player import Player
from networking.server.ClientConnection import ClientConnection
from util.constants import LEFT, RIGHT
from util.wonderUtils import ALL_WONDERS, get_wonder


async def create_players(clients: List[ClientConnection]) -> List[Player]:
    players = []
    await asyncio.gather(*(_create_player(client, players) for client in clients))
    _set_neighbors(players)
    return players


async def _create_player(client: ClientConnection, players: List[Player]) -> None:
    wonder_name = ""
    client.send_message("Enter your wonder")
    while wonder_name == "":
        msg = await client.get_message()

        if msg not in [wonder.name for wonder in ALL_WONDERS]:
            client.send_message("Invalid wonder name")

        elif msg in (player.wonder.name for player in players):
            client.send_message("Wonder in use")

        else:
            wonder_name = msg
    wonder = get_wonder(wonder_name)
    players.append(Player(client.name, wonder, client))


def _set_neighbors(players: List[Player]):
    left = players[-1]
    for player in players:
        player.neighbors[LEFT] = left
        player.neighbors[LEFT].neighbors[RIGHT] = player
        left = player
