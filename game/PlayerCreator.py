import asyncio
from typing import List, Optional

from game.Player import Player
from game.Wonder import Wonder
from networking.server.ClientConnection import ClientConnection
from util.constants import LEFT, RIGHT
from util.wonderUtils import create_wonders


async def create_players(clients: List[ClientConnection]) -> List[Player]:
    players = []
    await asyncio.gather(*(_create_player(client, players, clients) for client in clients))
    _set_neighbors(players)
    return players


async def _create_player(client: ClientConnection, players: List[Player], clients: List[ClientConnection]) -> None:
    wonders = create_wonders()
    all_wonder_names = [wonder.name.lower() for wonder in wonders]
    wonder_name = ""
    client.send_message("Enter your wonder")
    while wonder_name == "":
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

    wonder = get_wonder(wonder_name, wonders)
    player = Player(wonder, client)
    players.append(player)
    for c in clients:
        if player.client is not c:
            c.send_message(f"{player.name} has selected {wonder.name}")


def _set_neighbors(players: List[Player]):
    left = players[-1]
    for player in players:
        player.neighbors[LEFT] = left
        player.neighbors[LEFT].neighbors[RIGHT] = player
        left = player


def get_wonder(wonder_name: str, wonders: List[Wonder]) -> Optional[Wonder]:
    for wonder in wonders:
        if wonder.name.lower() == wonder_name.lower():
            return wonder
    print("Wonder not found!")
    return None
