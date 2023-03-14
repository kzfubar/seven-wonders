from __future__ import annotations

import json
from typing import List

from game.Card import Card
from game.Wonder import Wonder
from util.cardUtils import get_effects


def create_wonders() -> List[Wonder]:
    with open("resources/wonders.json") as f:
        data = json.load(f)
        return [
            Wonder(
                wonder["name"],
                wonder["resources"][0],
                [
                    Card(
                        -1,
                        f"{wonder['name']}{i}",
                        0,
                        "wonder_power",
                        card["cost"],
                        [],
                        get_effects({"effects": card["effects"], "type": "wonder"}, 0)[0],
                        # todo wonder effect id?
                    )
                    for i, card in enumerate(wonder["state"])
                ],
            )
            for wonder in data
        ]
