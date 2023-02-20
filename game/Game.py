from __future__ import annotations

import random
from abc import abstractmethod
from typing import Dict, List, Optional

from game.Card import Card
from game.Player import Player
from util.constants import LEFT, RIGHT


class Game:
    pass_order: Dict[int, str] = {1: LEFT, 2: RIGHT, 3: LEFT}
    age: int
    players: List[Player]
    cards: List[Card]

    def __str__(self):
        return f"players = {self._get_player_order()}"

    @abstractmethod
    def _message_players(self, message: str):
        pass

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

    @abstractmethod
    def _play_round(self):
        pass

    def play(self):
        self._message_players("starting game!")
        for age in range(1, 4):
            self.age = (
                age
            )  # TODO: is age an attribute, or is it getting passed to func? (curr. both)
            self._message_players(f"begin age: {self.age}")
            self._deal_cards(self.age)
            for round_number in range(6):
                self._message_players(f"begin round: {round_number}")
                self._play_round()
                self._end_round(self.age)
            self._end_age(self.age)
        self._end_game()
