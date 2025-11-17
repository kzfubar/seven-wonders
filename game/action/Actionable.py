from collections.abc import Callable
from typing import Any


class Actionable:
    def __init__(self, func: Callable[..., None], argv: list[Any]) -> None:
        self.func = func
        self.argv = argv

    def run(self) -> None:
        self.func(*self.argv)
