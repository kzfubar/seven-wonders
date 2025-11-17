import json
import pathlib
from typing import Any


class Config:
    def __init__(self) -> None:
        self.path = "./networking/config.json"
        with pathlib.Path(self.path).open("r", encoding="utf-8") as f:
            self.config = json.load(f)

    def get(self, key: str) -> Any:
        return self.config[key]

    def add(self, key: str, value: str) -> None:  # todo maybe don't add duplicates?
        values: list[Any] = self.config[key]
        values.append(value)
        with pathlib.Path(self.path).open("w", encoding="utf-8") as f:
            self.config[key] = values
            json.dump(self.config, f, indent=2)
