import re
from enum import Enum

ANSI_ESCAPE = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')


class ANSI(Enum):
    def __str__(self):
        return str(self.value)

    PURPLE = '\033[95m'
    BROWN = '\033[38;5;94m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = "\u001b[37m"
    BRIGHT_WHITE = "\u001b[97m"
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def use(c: ANSI, s: str) -> str:
    return str(c) + s + str(ANSI.END)


def linelen(s: str) -> int:
    return len(ANSI_ESCAPE.sub('', s))


def ansilen(s: str) -> int:
    return len(s) - linelen(s)
