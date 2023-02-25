MILITARY_POINTS = (0, 1, 3, 5)

TRADABLE_TYPES = set(("common", "luxury"))
LUXURY_GOODS = set("lgp")
COMMON_GOODS = set("wsbo")


LEFT = "left"
RIGHT = "right"
KNOWN_IP = "known_ip"

COINS = "coins"
RESOURCE_MAP = {
    # common
    "w": "wood",
    "s": "stone",
    "b": "brick",
    "o": "ore",
    # luxury
    "l": "loom",
    "g": "glass",
    "p": "paper",
    # token
    "v": "victory_point",
    "m": "military_might",
    "c": COINS,
    # science
    "y": "cog",
    "x": "compass",
    "z": "tablet",
}
