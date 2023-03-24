from util.ANSI import ANSI

MILITARY_POINTS_PER_AGE = (0, 1, 3, 5)
MAX_PLAYERS: int = 7

LUXURY_GOODS = set("lgp")
COMMON_GOODS = set("wsbo")

WONDER_POWER = "wonder_power"
WONDER_STAGE = "wonder_stage"
COMMON = "common"
LUXURY = "luxury"
CIVILIAN = "civilian"
COMMERCIAL = "commercial"
MILITARY = "military"
SCIENCE = "science"
GUILD = "guild"

TYPE_COLOR_MAP = {
    COMMON: ANSI.BROWN,
    LUXURY: ANSI.WHITE,
    CIVILIAN: ANSI.BLUE,
    COMMERCIAL: ANSI.YELLOW,
    MILITARY: ANSI.RED,
    SCIENCE: ANSI.GREEN,
    GUILD: ANSI.PURPLE,
}

TRADABLE_TYPES = set((COMMON, LUXURY, WONDER_POWER))

LEFT = "left"
RIGHT = "right"
KNOWN_IP = "known_ip"

COINS = "coins"
MILITARY_MIGHT = "military_might"
MILITARY_POINTS = "military_points"
DEFEAT = "defeat"

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
    "m": MILITARY_MIGHT,
    "c": COINS,
    # science
    "y": "cog",
    "x": "compass",
    "z": "tablet",
}
