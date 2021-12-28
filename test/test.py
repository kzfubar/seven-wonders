from game.Card import *

effects = {"victory": [Effect("victory", [("v", 1)], [], ["self"], False), Effect("victory", [("v", 2)], [], ["self"], False)]}

def get_victory() -> int:
    vp = 0
    for effect in effects["victory"]:
        vp += effect.resources[0][1]
    return vp

assert get_victory() == 3