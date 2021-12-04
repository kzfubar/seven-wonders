from Player import Player
from util import *


class Game:
    pass_order = {
        1: LEFT,
        2: RIGHT,
        3: LEFT
    }

    def __init__(self, num_players):
        print(f"creating game with {num_players}...")

        if num_players < 3:
            raise Exception("min players is 3, t-that's fine!")
        if num_players > len(ALL_WONDERS):
            raise Exception("more players than wonders, goober!")

        self.cards = get_all_cards(num_players)
        self.players = [Player(wonder) for wonder in random.sample(ALL_WONDERS, num_players)]
        self.__set_neighbors()

        [print(p) for p in self.players]

        print("game created")

    def __set_neighbors(self):
        for a, b, c in zip([self.players[-1]] + self.players, self.players, self.players + [self.players[0]]):
            b.neighbors[LEFT] = a
            b.neighbors[RIGHT] = c

    def __deal_cards(self, age: int):
        card_list = self.__get_cards(age)
        random.shuffle(card_list)

        for i, player in enumerate(self.players):
            player.hand = card_list[i * 7: (i + 1) * 7]

    def __play_round(self, age: int):
        self.__deal_cards(age)
        for i in range(6):
            print(f"begin round: {i}")
            for player_number, player in enumerate(self.players):
                print(f"Player {player_number}'s turn")
                print(f"your hand is:\n{player.hand_to_str()}")

                player_input = input("(p)lay, (d)iscard, (b)ury a card: ")
                action, card_index = player_input[0], int(player_input[1])

                self.__get_player(player_number).take_action(action, card_index)
            self.__pass_hands(age)
        # todo calculate victory points

    def __get_cards(self, age: int):
        return [card for card in self.cards if card.age == age]

    def __get_player(self, player_number: int):
        return self.players[player_number]

    def __pass_hands(self, age: int):
        player_order = self.players + [self.players[0]]

        if self.pass_order[age] == LEFT:
            player_order.reverse()

        temp_hand = []
        for player in player_order:
            player.hand, temp_hand = temp_hand, player.hand

    def play(self):
        print("starting game!")
        for age in range(1, 4):
            print(f"begin age: {age}")
            self.__play_round(age)
