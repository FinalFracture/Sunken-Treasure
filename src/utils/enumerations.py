from enum import IntEnum, auto

class ViewID(IntEnum):
    NULL = 0
    OVERWORLD = auto()
    INVENTORY = auto()
    TRADE = auto()
    UPGRADE = auto()

class CardID(IntEnum):
    NULL = 0
    COIN = auto()
    CARGO = auto()
    BEARING = auto()
    SPEED = auto()
    WEATHER = auto()
    TIME = auto()
    WIND = auto()