import asyncio

from game.Player import Player
from game.Side import Side
from networking.server.ClientConnection import ClientConnection
from util.constants import LEFT, RIGHT
from util.wonderUtils import create_wonders


async def create_players(clients: list[ClientConnection]) -> list[Player]:
    players = []
    await asyncio.gather(
        *(_create_player(client, players, clients) for client in clients)
    )
    _set_neighbors(players)
    return players


async def _create_player(
    client: ClientConnection, players: list[Player], clients: list[ClientConnection]
) -> None:
    wonders = create_wonders()
    all_wonder_names = wonders.keys()
    wonder_name = ""
    side = Side.A
    client.clear_message_buffer()
    client.send_message("Enter your wonder")
    while not wonder_name:
        # todo wonder options should be client side
        client.send_event(
            "game", {"type": "wonder_selection", "options": ["r", "b", "g", "e", "a"]}
        )
        msg = await client.get_message()
        args: list[str] = msg.split()
        selected_wonder_name = args.pop(0)
        matched_wonder_names = [
            wn
            for wn in all_wonder_names
            if wn.lower().startswith(selected_wonder_name.lower())
        ]
        if len(matched_wonder_names) == 0:
            client.send_message("Invalid wonder name")
            continue
        if len(matched_wonder_names) > 1:
            client.send_message(
                f"Please specify wonder: '{selected_wonder_name}' matched to {matched_wonder_names}"
            )
            continue

        matched_wonder_name = matched_wonder_names[0]
        if matched_wonder_name in (player.wonder.base_name for player in players):
            client.send_message("Wonder in use")
        else:
            wonder_name = matched_wonder_name

        try:
            if args:
                side = Side(args[0].upper())
        except ValueError:
            client.send_message(f"Invalid side {args[0]}")
            wonder_name = ""

    wonder = wonders[wonder_name][side.value]
    player = Player(wonder, client)
    players.append(player)
    for c in clients:
        if player.client is not c:
            c.send_message(f"{player.name} has selected {wonder.name}")


def _set_neighbors(players: list[Player]) -> None:
    left = players[-1]
    for player in players:
        player.neighbors[LEFT] = left
        left.neighbors[RIGHT] = player
        left = player
