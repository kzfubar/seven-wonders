from util.constants import (COINS, MILITARY_MIGHT, MILITARY_POINTS, DEFEAT, COMMON, LUXURY, CIVILIAN, COMMERCIAL,
                            MILITARY, SCIENCE, GUILD)


class Tableau:
    def __init__(self):
        self.tokens = {
            COINS: 0,
            MILITARY_MIGHT: 0,
            MILITARY_POINTS: 0,
            DEFEAT: 0
        }
        self.card_types_played = {
            COMMON: 0,
            LUXURY: 0,
            CIVILIAN: 0,
            COMMERCIAL: 0,
            MILITARY: 0,
            SCIENCE: 0,
            GUILD: 0
        }

    def count(self, token: str) -> int:
        if token in self.tokens:
            return self.tokens[token]
        if token in self.card_types_played[token]:
            return self.card_types_played[token]
        raise KeyError

    def add(self, token: str, count: int) -> bool:
        try:
            self.tokens[token] += count
            return True
        except KeyError:
            return False

    def add_card_type(self, card_type: str) -> bool:
        try:
            self.card_types_played[card_type] += 1
            return True
        except KeyError:
            return False
