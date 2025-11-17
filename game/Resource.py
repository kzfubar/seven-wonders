from dataclasses import dataclass


@dataclass
class Resource:
    key: str
    amount: int
