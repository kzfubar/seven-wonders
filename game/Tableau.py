from util.ANSI import ANSI, use
from util.constants import (
    CIVILIAN,
    COINS,
    COMMERCIAL,
    COMMON,
    DEFEAT,
    GUILD,
    LUXURY,
    MILITARY,
    MILITARY_MIGHT,
    MILITARY_POINTS,
    SCIENCE,
    TYPE_COLOR_MAP,
    WONDER_POWER,
    WONDER_STAGE,
)


class Tableau:
    def __init__(self) -> None:
        self.tokens = {COINS: 0, MILITARY_MIGHT: 0, MILITARY_POINTS: 0, DEFEAT: 0}
        self.card_types_played = {
            WONDER_STAGE: 0,
            WONDER_POWER: 0,
            COMMON: 0,
            LUXURY: 0,
            CIVILIAN: 0,
            COMMERCIAL: 0,
            MILITARY: 0,
            SCIENCE: 0,
            GUILD: 0,
        }

    def __str__(self) -> str:
        return self.token_info() + "\n" + self.card_type_info()

    def token_info(self) -> str:
        tok_l: list[str] = []
        for token, count in self.tokens.items():
            tok_l.append(f"{token}: {count}")
        return ", ".join(tok_l)

    def card_type_info(self) -> str:
        types_l: list[str] = []
        for card_type, count in self.card_types_played.items():
            color = TYPE_COLOR_MAP.get(card_type, ANSI.BRIGHT_WHITE)
            types_l.append(f"{use(color, card_type)}: {count}")
        return ", ".join(types_l)

    def count(self, token: str) -> int:
        if token in self.tokens:
            return self.tokens[token]
        if token in self.card_types_played:
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
