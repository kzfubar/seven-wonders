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
    all_wonder_names = [wonder.name.lower() for wonder in ALL_WONDERS]
    wonder_name = ""
    client.send_message("Enter your wonder")
    while wonder_name == "":
        client.clear_message_buffer()
        msg = await client.get_message()

        matched_wonders = [wn for wn in all_wonder_names if wn.startswith(msg.lower())]
        if len(matched_wonders) == 0:
            client.send_message("Invalid wonder name")
            continue
        elif len(matched_wonders) > 1:
            client.send_message("Please specify wonder")
            continue

        wn = matched_wonders[0]
        if wn in (player.wonder.name.lower() for player in players):
            client.send_message("Wonder in use")
        else:
            wonder_name = wn

    wonder = get_wonder(wonder_name)
    players.append(Player(wonder, client))


def _set_neighbors(players: List[Player]):
    left = players[-1]
    for player in players:
        player.neighbors[LEFT] = left
        player.neighbors[LEFT].neighbors[RIGHT] = player
        left = player
