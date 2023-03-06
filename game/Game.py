from __future__ import annotations

import asyncio
import random
from collections import defaultdict
from typing import Dict, List, Tuple

from game.PlayerCreator import create_players
from game.Card import Card, resource_to_human
from game.Player import Player
from game.PlayerActionPhase import PlayerActionPhase
from networking.server.ClientConnection import ClientConnection
from util.cardUtils import get_all_cards
from util.constants import LEFT, RIGHT, MAX_PLAYERS


class Game:
    NUM_ROUNDS: int = 7
    age: int
    player_action_phase: PlayerActionPhase

    def __init__(self):
        pass

    def __str__(self):
        return f"players = {self._get_player_order()}"

    async def start(self, clients: List[ClientConnection]):
        await self._start(clients)
        asyncio.create_task(self.play())

    async def _start(self, clients: List[ClientConnection]):
        num_players = len(clients)
        if num_players < 3:
            raise Exception(
                f"min players is 3, cannot start the game with {num_players}"
            )
            # todo make this actually message the player with error
        if num_players > MAX_PLAYERS:
            raise Exception(
                f"more players than wonders, cannot start the game with {num_players}"
            )

        self.players = []
        self.players = await create_players(clients)
        self.players_by_client: Dict[ClientConnection, Player] = {
            p.client: p for p in self.players
        }
        self.players_by_name: Dict[str, Player] = {p.name: p for p in self.players}

        self.cards: List[Card] = get_all_cards(num_players)
        self.pass_order: Dict[int, str] = {1: LEFT, 2: RIGHT, 3: LEFT}
        self.player_action_phase = PlayerActionPhase(self.players)

        self._message_players(f"creating game with {num_players}...")
        [print(p) for p in self.players]
        print("game created")

    def _message_players(self, message: str):
        for player in self.players:
            player.display(message)

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
            player.hand = card_list[i :: len(self.players)]

    def _get_cards_for_age(self, age: int) -> List[Card]:
        return [card for card in self.cards if card.age == age]

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

    async def _end_round(self, round_number: int, age: int):
        if round_number == self.NUM_ROUNDS - 1:
            [player.discard_hand() for player in self.players]
        # do player end rounds synchronously, future expansions introduce end round effect order
        for player in self.players:
            await self.player_action_phase.end_round(player)
        for player in self.players:
            player.display(player.consolidated_effects())
        self._pass_hands(self.pass_order[age])
        self._update_coins()

    def _update_military(self, age: int):
        for player in self.players:
            self.player_action_phase.run_military(player, age)

    def _end_age(self, age: int):
        self._update_military(age)
        for player in self.players:
            self._message_players(
                f"{player.name} has {player.board['victory_points']} victory points!"
            )
            self._message_players(
                f"{player.name} has {player.board['military_points']} military points!"
            )
            self._message_players(f"{player.name} has {player.board['shame']} shame!\n")
            # todo add more?
            player.enable_flags()
        pass

    def _end_game(self):
        player_points: List[Tuple[str, int]] = []
        for player in self.players:
            player_points.append((player.name, sum(player.get_victory().values())))
        player_points.sort(key=lambda x: x[1], reverse=True)
        self._message_players(
            f"{player_points[0][0]} wins with {player_points[0][1]} points!"
        )
        self._message_players(f"{player_points} total point count")
        self._message_players(
            f"overall point distribution: {player_points}"
        )

    async def play(self):
        self._message_players("starting game!")
        for age in range(1, 4):
            self.age = age
            self._message_players(f"begin age: {self.age}")
            self._deal_cards(self.age)
            for round_number in range(1, self.NUM_ROUNDS):
                self._message_players(f"begin round: {round_number}")
                await self.player_action_phase.select_actions()
                self.player_action_phase.execute_actions()
                await self._end_round(round_number, self.age)
            self._end_age(self.age)
        self._end_game()
