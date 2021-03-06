from dataclasses import (
    asdict,
    dataclass,
)
from datetime import datetime
from typing import (
    Iterable,
    Optional,
)

from .enum import (
    Cell,
    Player,
)

__all__ = (
    'Moves',
    'BoardType',
    'GameMove',
    'GameMoves',
    'XOGame',
    'XOGames',
    'Position',
)

Moves = Iterable[tuple[int, Cell]]
BoardType = list[list[Cell]]
Position = tuple[int, int]


@dataclass(frozen=True, repr=True)
class GameMove:
    player: Player
    order: int
    row: int
    column: int
    created_at: datetime

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True, repr=True)
class XOGame:
    id: int
    user_id: int
    size: int
    winner: Optional[int]
    created_at: datetime
    finished_at: datetime

    def to_dict(self):
        return asdict(self)


GameMoves = Iterable[GameMove]
XOGames = Iterable[XOGame]
