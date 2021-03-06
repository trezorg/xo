from typing import (
    Iterable,
)

from .enum import Cell

__all__ = (
    'Motions',
    'BoardType',
)

Motions = Iterable[tuple[int, Cell]]
BoardType = list[list[Cell]]
