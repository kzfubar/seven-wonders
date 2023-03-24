from __future__ import annotations

import json
from typing import List

from game.Card import Card
from game.Wonder import Wonder
from util.cardUtils import get_effects, to_card_id
from util.constants import WONDER_STAGE, WONDER_POWER


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
                    card_type=WONDER_STAGE,
                    cost=card["cost"],
                    coupons=[],
                    effects=get_effects({"effects": card["effects"], "type": WONDER_STAGE}, stage_id),
                ))
            wonders.append(Wonder(
                name=wonder["name"],
                power=Card(card_id=wonder["name"],
                           name=wonder["name"],
                           age=0,
                           card_type=WONDER_POWER,
                           cost=[],
                           coupons=[],
                           effects=get_effects({"effects": wonder["power"], "type": WONDER_POWER}, wonder["name"])),
                stages=wonder_stages,
            ))
        return wonders
