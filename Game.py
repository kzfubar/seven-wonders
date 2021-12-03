import random

from Player import Player
from util import *


class Game:
    def __init__(self, num_players):
        print(f"creating game with {num_players}...")

        if num_players < 3:
            raise Exception("min players is 3, t-that's fine!")
        if num_players > len(all_wonders):
            raise Exception("more players than wonders, goober!")

        self.cards = get_all_cards(num_players)
        self.players = [Player(wonder) for wonder in random.sample(all_wonders, num_players)]
        self.set_neighbors()

        [print(p) for p in self.players]

        print("game created")

    def set_neighbors(self):
        for a, b, c in zip([self.players[-1]] + self.players, self.players, self.players + [self.players[0]]):
            b.left = a
            b.right = c

    def deal_cards(self, age: int):
        card_list = self.get_cards(age)
        random.shuffle(card_list)

        for i, player in enumerate(self.players):
            player.hand = card_list[i * 7: (i + 1) * 7]

    def play(self):
        for age in range(3):
            self.play_round(age)

    def play_round(self, age: int):
        self.deal_cards(age)
        for i in range(6):
            for player_number, player in enumerate(self.players):
                print(f"Player {player_number}'s turn")
                print(f"your hand is {player.hand}")

        print("starting game!")

    def get_cards(self, age: int):
        return [Card([], []) for _ in range(21)]