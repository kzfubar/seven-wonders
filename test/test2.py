from game.Card import Effect
from util.constants import COINS, COMMON, LUXURY

effects = {
    "victory": [
        Effect("victory", [("v", 2)], [LUXURY, COMMON], ["self"], False),
        Effect("victory", [("v", 2)], [], ["self"], False),
    ]
}
board = {
    "shame": 0,
    "military_points": 0,
    COINS: 3,
    COMMON: 1,
    LUXURY: 1,
    "civilian": 0,
    "commercial": 0,
    "military": 0,
    "science": 0,
    "guild": 0,
}


def get_victory():
    vp = 0
    for effect in effects["victory"]:
        if effect.target:
            for targets in effect.target:
                vp += board[targets] * effect.resources[0][1]
                print(effect.resources[0][0])
        else:
            vp += effect.resources[0][1]
    print(vp)
    return vp


assert get_victory() == 6
