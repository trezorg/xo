from enum import IntEnum

__all__ = (
    'Winner',
    'Player',
    'Cell',
)


class Cell(IntEnum):

    none = 0
    player = 1
    computer = 2


class Winner(IntEnum):

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


class Player(IntEnum):

    player = 1
    computer = 2
