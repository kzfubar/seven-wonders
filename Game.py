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
        self.players = [Player(str(i), wonder) for i, wonder in enumerate(random.sample(ALL_WONDERS, num_players))]
        self.__set_neighbors()

        [print(p) for p in self.players]

        print("game created")

    def _set_neighbors(self):
        for a, b, c in zip([self.players[-1]] + self.players, self.players, self.players + [self.players[0]]):
            b.neighbors[LEFT] = a
            b.neighbors[RIGHT] = c

    def _deal_cards(self, age: int):
        card_list = self._get_cards(age)
        random.shuffle(card_list)

        for i, player in enumerate(self.players):
            player.hand = card_list[i * 7: (i + 1) * 7]

    def _play_round(self, age: int):
        self._deal_cards(age)
        for i in range(6):
            print(f"begin round: {i}")
            for player_number, player in enumerate(self.players):
                print(f"{player.name}'s turn")
                print(f"your hand is:\n{player.hand_to_str()}")
                print(f"Bury cost: {min_cost(player.get_payment_options(player.wonder.get_next_power()))}")

                player_input = input("(p)lay, (d)iscard or (b)ury a card: ")
                action, card_index = player_input[0], int(player_input[1])

                player.take_action(action, card_index)
            self._pass_hands(age)
        # todo calculate victory points

    def _get_cards(self, age: int) -> List[Card]:
        return [card for card in self.cards if card.age == age]

    def _get_player(self, player_number: int) -> Player:
        return self.players[player_number]

    def _pass_hands(self, age: int):
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
            self._play_round(age)
