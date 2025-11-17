from __future__ import annotations

import json
import pathlib
from collections import defaultdict

from game.Card import Card
from game.Side import Side
from game.Wonder import Wonder
from util.cardUtils import get_effects, to_card_id
from util.constants import WONDER_POWER, WONDER_STAGE


def _to_wonder_name(wonder_data: dict) -> str:
    base_name = wonder_data["name"]
    side = wonder_data["side"]
    return f"{base_name} ({side})"


def _create_wonders(wonders_data: dict) -> list[Wonder]:
    wonders = []
    for wonder_data in wonders_data:
        wonder_name = _to_wonder_name(wonder_data)
        wonder_stages = []
        for i, card in enumerate(wonder_data["stages"]):
            stage_name = f"{wonder_name} Stage {i}"
            stage_id = to_card_id(stage_name)
            wonder_stages.append(
                Card(
                    card_id=stage_id,
                    name=stage_name,
                    age=0,
                    card_type=WONDER_STAGE,
                    cost=card["cost"],
                    effects=get_effects(
                        {"effects": card["effects"], "type": WONDER_STAGE}, stage_id
                    ),
                )
            )
        wonders.append(
            Wonder(
                name=wonder_name,
                base_name=wonder_data["name"],
                side=Side(wonder_data["side"]),
                power=Card(
                    card_id=wonder_name,
                    name=wonder_name,
                    age=0,
                    card_type=WONDER_POWER,
                    cost=[],
                    effects=get_effects(
                        {"effects": wonder_data["power"], "type": WONDER_POWER},
                        wonder_name,
                    ),
                ),
                stages=wonder_stages,
            )
        )
    return wonders


def create_wonders() -> dict[str, dict[str, Wonder]]:
    """wonder base name lowercase : Side : Wonder"""
    wonders: list[Wonder] = []
    with pathlib.Path("resources/wondersA.json").open(encoding="utf-8") as f:
        data = json.load(f)
        wonders += _create_wonders(data["wonders"])
    with pathlib.Path("resources/wondersB.json").open(encoding="utf-8") as f:
        data = json.load(f)
        wonders += _create_wonders(data["wonders"])

    wonders_dict = defaultdict(dict)
    for wonder in wonders:
        wonders_dict[wonder.base_name][wonder.side] = wonder
    return dict(wonders_dict)
