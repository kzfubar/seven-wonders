from game.Flag import Flag


class FlagHolder:
    flag: Flag
    enabled: bool

    def __init__(self, flag: Flag):
        self.flag = flag
        self.enabled = True

    def contains(self, flag: Flag) -> bool:
        return self.flag == flag

    def is_enabled(self) -> bool:
        return self.enabled

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False
