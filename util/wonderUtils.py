from __future__ import annotations
from game.Wonder import Wonder

import json
import pprint
from typing import Optional, List

from game.Card import Card
from util.cardUtils import get_effects


def all_wonders() -> List[Wonder]:
    with open("resources/wonders.json") as f:
        data = json.load(f)
        return [
            Wonder(
                wonder["name"],
                wonder["resources"][0],
                [
                    Card(
                        f"{wonder['name']}{i}",
                        0,
                        "wonder_power",
                        card["cost"],
                        [],
                        get_effects({"effects": card["effects"], "type": "wonder"}),
                    )
                    for i, card in enumerate(wonder["state"])
                ],
            )
            for wonder in data
        ]


def get_wonder(wonder_name: str) -> Optional[Wonder]:
    for wonder in ALL_WONDERS:
        if wonder.name.lower() == wonder_name.lower():
            return wonder
    print("Wonder not found!")
    return None


ALL_WONDERS = all_wonders()
pprint.pprint(ALL_WONDERS)
