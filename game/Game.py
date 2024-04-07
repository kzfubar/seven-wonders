from __future__ import annotations

import random
from typing import Dict, List, Tuple

from game.Card import Card
from game.Player import Player
from game.PlayerActionPhase import PlayerActionPhase
from game.PlayerCreator import create_players
from game.VictoryCalculator import VictoryCalculator
from game.action import Action
from networking.server.ClientConnection import ClientConnection
from util.cardUtils import get_all_cards
from util.constants import LEFT, RIGHT, MAX_PLAYERS
from util.toggles import EOR_EFFECTS


class Game:
    NUM_ROUNDS: int = 7
    age: int
    player_action_phase: PlayerActionPhase

    def __init__(self):
        self.running = False
        self.player_clients: List[ClientConnection] = []
        self.spectate_clients: List[ClientConnection] = []

    def __str__(self):
        return f"players = {self._get_player_order()}"

    async def start(self, clients: List[ClientConnection]):
        self.running = True
        self.player_clients += [
            client for client in clients if client not in self.spectate_clients
        ]
        await self._start()
        await self._play()

    async def _start(self):
        num_players = len(self.player_clients)
        if num_players < 3:
            raise Exception(
                f"min players is 3, cannot start the game with {num_players}"
            )
            # todo make this actually message the player with error
        if num_players > MAX_PLAYERS:
            raise Exception(
                f"more players than wonders, cannot start the game with {num_players}"
            )

        self.players: List[Player] = []
        self.players = await create_players(self.player_clients)
        self.players_by_client: Dict[ClientConnection, Player] = {
            p.client: p for p in self.players
        }
        self.players_by_name: Dict[str, Player] = {p.name: p for p in self.players}

        self.cards: List[Card] = get_all_cards(num_players)
        self.victory_calculator = VictoryCalculator(self.cards)
        self.pass_order: Dict[int, str] = {1: LEFT, 2: RIGHT, 3: LEFT}
        self.player_action_phase = PlayerActionPhase(self.players)

        self._message_players(f"creating game with {num_players}...")
        [print(p) for p in self.players]
        print("game created")

    def _message_players(self, message: str):
        for player in self.players:
            player.display(message)
        for client in self.spectate_clients:
            client.send_message(message)

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
            player.hand = sorted(player.hand, key=lambda card: card.card_type)

    def _get_cards_for_age(self, age: int) -> List[Card]:
        return [card for card in self.cards if card.age == age]

    def _pass_hands(self, direction: str):
        player_order = self.players + [self.players[0]]
        if direction == LEFT:
            player_order.reverse()
        temp_hand: List[Card] = []
        for player in player_order:
            player.hand, temp_hand = temp_hand, player.hand
        for player in player_order:
            player.hand = sorted(player.hand, key=lambda card: card.card_type)

    def _update_coins(self):
        for player in self.players:
            player.update_coins()

    async def _end_round(self, round_number: int, age: int):
        if round_number == self.NUM_ROUNDS - 1:
            for player in self.players:
                await self.player_action_phase.last_round(player)
            [player.discard_hand() for player in self.players]
        # do player end rounds synchronously, future expansions introduce end round effect order
        for player in self.players:
            await self.player_action_phase.end_round(player)
        for player in self.players:
            if player.toggles[EOR_EFFECTS]:
                player.display(player.consolidated_effects())
        self._pass_hands(self.pass_order[age])
        self._update_coins()

    def _update_military(self, age: int):
        for player in self.players:
            self.player_action_phase.run_military(player, age)

    async def _end_age(self, age: int):
        self._update_military(age)
        for player in self.players:
            self._message_players(
                f"{player.name} has {player.military_points()} military points!"
            )
            self._message_players(f"{player.name} has {player.defeat()} defeats!\n")
            await self.player_action_phase.end_age(player, age)

    def _end_game(self):
        player_points: List[Tuple[str, int]] = []
        for player in self.players:
            player_vp = self.victory_calculator.get_victory(player)
            self._message_players(f"{player.name} has {player_vp}")
            player_points.append((player.name, sum(player_vp.values())))
        player_points.sort(key=lambda x: x[1], reverse=True)
        self._message_players(f"{player_points} total point count")
        self._message_players(
            f"{player_points[0][0]} wins with {player_points[0][1]} points!"
        )
        self.running = False

    async def _play(self):
        self._message_players("starting game!")
        for player in self.players:
            Action.activate_card(player, player.wonder.power)
        for age in range(1, 4):
            self.age = age
            self._message_players(f"begin age: {self.age}")
            self._deal_cards(self.age)
            for round_number in range(1, self.NUM_ROUNDS):
                self._message_players(f"begin round: {round_number}")
                await self.player_action_phase.select_actions()
                self.player_action_phase.execute_actions()
                await self._end_round(round_number, self.age)
            await self._end_age(self.age)
        self._end_game()
