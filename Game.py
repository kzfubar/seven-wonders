from Player import Player
from util import *


class Game:
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
            b.left = a
            b.right = c

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

                self.__take_action(player_number, action, card_index)

    def __take_action(self, player_number: int, action: str, card_index: int):
        card = self.__get_player(player_number).get_card(card_index)
        if action == 'p':
            print(f"playing {card}")
            self.__play()
        elif action == 'd':
            print(f"discarding {card}")
            self.__discard()
        elif action == 'b':
            print(f"burying {card}")
            self.__bury()
        else:
            raise Exception("we currently don't handle invalid actions!")  # todo

    def __play(self):
        pass

    def __discard(self):
        pass

    def __bury(self):
        pass

    def __get_cards(self, age: int):
        return [card for card in self.cards if card.age == age]

    def __get_player(self, player_number: int):
        return self.players[player_number]

    def play(self):
        print("starting game!")
        for age in range(1, 4):
            print(f"begin age: {age}")
            self.__play_round(age)
