from abc import abstractmethod
from typing import Dict

from Player import Player
from util.util import *


class Game:
    pass_order: Dict[int, str] = {
        1: LEFT,
        2: RIGHT,
        3: LEFT
    }

    @abstractmethod
    def __init__(self, players: List[Player]):
        self.players: List[Player] = players
        self.cards = get_all_cards(len(players))
        self._set_neighbors()

        [print(p) for p in self.players]  # todo debug logging (remove this?)
        print("game created")

    @abstractmethod
    def _message_players(self, message: str):
        pass

    def _set_neighbors(self):
        for a, b, c in zip([self.players[-1]] + self.players, self.players, self.players + [self.players[0]]):
            b.neighbors[LEFT] = a
            b.neighbors[RIGHT] = c

    def _deal_cards(self, age: int):
        card_list = self._get_cards_for_age(age)
        random.shuffle(card_list)
        for i, player in enumerate(self.players):
            player.hand = card_list[i * 7: (i + 1) * 7]

    def _get_cards_for_age(self, age: int) -> List[Card]:
        return [card for card in self.cards if card.age == age]

    def _get_player(self, player_number: int) -> Player:
        return self.players[player_number]

    def _pass_hands(self, direction: str):
        player_order = self.players + [self.players[0]]
        if direction == LEFT:
            player_order.reverse()
        temp_hand = []
        for player in player_order:
            player.hand, temp_hand = temp_hand, player.hand

    def _end_round(self, age: int):
        self._pass_hands(self.pass_order[age])

    def _end_age(self):
        pass

    def _end_game(self):
        pass  # todo calculate victory points

    def play(self):
        self._message_players("starting game!")
        for age in range(1, 4):
            self._message_players(f"begin age: {age}")
            self._deal_cards(age)
            for round_number in range(6):
                self._message_players(f"begin round: {round_number}")
                for player_number, player in enumerate(self.players):
                    print(f"{player.name}'s turn")
                    turn_over = False
                    while not turn_over:
                        turn_over = player.take_turn()
                self._end_round(age)
            self._end_age()
        self._end_game()

