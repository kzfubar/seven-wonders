import json
from typing import Any, List


class Config:
    def __init__(self):
        self.path = "./resources/config.json"
        with open(self.path, 'r') as f:
            self.config = json.load(f)

    def get(self, key: str) -> Any:
        return self.config[key]

    def add(self, key: str, value: str):  # todo maybe don't add duplicates?
        values: List[Any] = self.config[key]
        values.append(value)
        with open(self.path, 'w') as f:
            self.config[key] = values
            json.dump(self.config, f, indent=2)

