from enum import (
    Enum,
    IntEnum,
    unique,
)
from typing import (
    Dict,
    Tuple,
)
from functools import lru_cache
from operator import attrgetter

__all__ = (
    'Winner',
    'Player',
    'Cell',
)


@unique
class BaseEnum(Enum):

    @classmethod
    @lru_cache(None)
    def values(cls) -> Tuple:
        return tuple(map(attrgetter('value'), cls))

    @classmethod
    @lru_cache(None)
    def names(cls) -> Tuple:
        return tuple(map(attrgetter('name'), cls))

    @classmethod
    @lru_cache(None)
    def items(cls) -> Tuple:
        return tuple(zip(cls.values(), cls.names()))

    @classmethod
    @lru_cache(None)
    def members(cls) -> Dict:
        return dict(cls.items())


class Cell(BaseEnum, IntEnum):

    none = 0
    player = 1
    computer = 2

    def __str__(self):
        if self == Cell.none:
            return ' '
        if self == Cell.player:
            return 'x'
        return '0'


class Winner(BaseEnum, IntEnum):

    none = 0
    player = 1
    computer = 2

    @classmethod
    def from_cell(cls, cell: Cell):
        return cls(cell.value)

    def __bool__(self):
        if self == Winner.none:
            return False
        return True


class Player(BaseEnum, IntEnum):

    player = 1
    computer = 2
