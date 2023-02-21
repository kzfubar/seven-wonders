from __future__ import annotations

import asyncio
import random
from typing import Dict, List, Optional

from game.Card import Card
from game.Player import Player
from networking.server.ClientConnection import ClientConnection
from util.cardUtils import get_all_cards
from util.constants import LEFT, RIGHT
from util.wonderUtils import ALL_WONDERS, get_wonder


class Game:
    players: List[Player] = []
    cards: List[Card] = []
    pass_order: Dict[int, str] = {1: LEFT, 2: RIGHT, 3: LEFT}
    age: int = 0

    def __str__(self):
        return f"players = {self._get_player_order()}"

    async def add_clients(self, clients: List[ClientConnection]):
        num_players = len(clients)
        if num_players < 3:
            raise Exception(f"min players is 3, cannot start the game with {num_players}")
            # todo make this actually message the player with error
        if num_players > len(ALL_WONDERS):
            raise Exception(f"more players than wonders, cannot start the game with {num_players}")
        self._message_players(f"creating game with {num_players}...")

        await asyncio.gather(*(self._create_player(client) for client in clients))
        self.cards = get_all_cards(num_players)
        self._set_neighbors()

        [print(p) for p in self.players]  # todo debug logging (remove this?)
        print("game created")

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
        self.players.append(Player(client.name, wonder, client))

    def _message_players(self, message: str):
        for player in self.players:
            player.display(message)

    def _set_neighbors(self):
        left = self.players[-1]
        for player in self.players:
            player.neighbors[LEFT] = left
            player.neighbors[LEFT].neighbors[RIGHT] = player
            left = player

    def _get_player_order(self) -> str:
        start = self.players[0]
        player_order: List[str] = [start.name]
        player = start.neighbors[RIGHT]
        while player is not start:
            player_order.append(player.name)
            player = player.neighbors[RIGHT]
        pass_icon = "<-" if self.pass_order[self.age] == LEFT else "->"
        return pass_icon.join(player_order)

    def _deal_cards(self, age: int):
        card_list = self._get_cards_for_age(age)
        random.shuffle(card_list)
        for i, player in enumerate(self.players):
            player.hand = card_list[i:: len(self.players)]

    def _get_cards_for_age(self, age: int) -> List[Card]:
        return [card for card in self.cards if card.age == age]

    # todo handle duplicate player names?
    def get_player(self, player_name: str) -> Optional[Player]:
        for player in self.players:
            if player.name == player_name:
                return player
        return None

    def _pass_hands(self, direction: str):
        player_order = self.players + [self.players[0]]
        if direction == LEFT:
            player_order.reverse()
        temp_hand = []
        for player in player_order:
            player.hand, temp_hand = temp_hand, player.hand

    def _update_coins(self):
        for player in self.players:
            player.update_coins()

    async def _play_round(self, player: Player):
        player.display(f"{player.name}, take your turn")
        await player.take_turn()
        player.display(player.effects)

    def _end_round(self, age: int):
        self._pass_hands(self.pass_order[age])
        self._update_coins()

    def _update_military(self, age: int):
        for player in self.players:
            player.run_military(age)

    def _end_age(self, age: int):
        self._update_military(age)
        for player in self.players:
            print(player)
        pass

    def _end_game(self):
        pass  # todo calculate victory points

    async def play(self):
        self._message_players("starting game!")
        for age in range(1, 4):
            self.age = age
            self._message_players(f"begin age: {self.age}")
            self._deal_cards(self.age)
            for round_number in range(6):
                self._message_players(f"begin round: {round_number}")
                await asyncio.gather(*(self._play_round(player) for player in self.players))
                self._end_round(self.age)
            self._end_age(self.age)
        self._end_game()
