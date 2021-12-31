from __future__ import annotations

from abc import abstractmethod
from typing import List, Optional, Dict

from game import Player


class Menu:
    def __init__(self, player: Player.Player):
        self.player = player
        self.options: Dict[str, MenuOption] = {option.command: option(self) for option in MenuOption.__subclasses__()}

    def get_options_str(self) -> str:
        return '\n'.join([f"({option.command}) {option.display_text}" for option in self.options.values()])


class MenuOption:
    display_text: str
    command: str

    def __init__(self, menu: Menu):
        self.menu: Menu = menu

    @abstractmethod
    def get_response(self, args: Optional[List[str]] = None):
        pass


class MenuPlayer(MenuOption):
    display_text: str = "Display player information"  # todo tell user that they can supply a player name
    command: str = 'p'

    def get_response(self, args: Optional[List[str]] = None):
        return self.menu.player.game.get_player(args[0]) if args else self.menu.player


class MenuGame(MenuOption):
    display_text: str = "Display game information"
    command: str = 'g'

    def get_response(self, args: Optional[List[str]] = None):
        return self.menu.player.game
