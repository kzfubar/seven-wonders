from __future__ import annotations

import json
from typing import List

from game.Card import Card
from game.Wonder import Wonder
from util.cardUtils import get_effects, to_card_id


def create_wonders() -> List[Wonder]:
    with open("resources/wonders.json") as f:
        data = json.load(f)
        wonders = []
        for wonder in data:
            wonder_stages = []
            for i, card in enumerate(wonder["stages"]):
                stage_name = f"{wonder['name']}{i}"
                stage_id = to_card_id(stage_name)
                wonder_stages.append(Card(
                    card_id=stage_id,
                    name=stage_name,
                    age=0,
                    card_type="wonder_stage",
                    cost=card["cost"],
                    coupons=[],
                    effects=get_effects({"effects": card["effects"], "type": "wonder"}, stage_id),
                ))
            wonders.append(Wonder(
                name=wonder["name"],
                power=Card(card_id=wonder["name"],
                           name=wonder["name"],
                           age=0,
                           card_type="wonder_power",
                           cost=[],
                           coupons=[],
                           effects=get_effects({"effects": wonder["power"], "type": "wonder"}, wonder["name"])),
                stages=wonder_stages,
            ))
        return wonders
