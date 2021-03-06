from typing import (
    Iterable,
    Literal,
)

from .enum import Cell

__all__ = (
    'Motions',
    'BoardType',
)

Motions = Iterable[tuple[int, Literal[Cell.player, Cell.computer]]]
BoardType = list[list[Cell]]
