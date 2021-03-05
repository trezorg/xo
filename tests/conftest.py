from typing import Optional

import pytest
from app.xo import (
    Board,
    Cell,
)


def board(size: Optional[int] = None, content: Optional[list[Cell]] = None):

    @pytest.fixture
    def _board():
        if content is None and size is None:
            raise ValueError('Wrong function arguments. At least one, either size or content should be set')
        if content is not None:
            return Board.create(content)
        return Board(size)

    return _board


blank_3_board = board(size=3)
diagonal_player_winner_board_size_3 = board(
    content=[
        Cell.player,
        Cell.none,
        Cell.none,
        Cell.none,
        Cell.player,
        Cell.none,
        Cell.none,
        Cell.none,
        Cell.player,
    ]
)
row_player_winner_board_size_3 = board(
    content=[
        Cell.player,
        Cell.player,
        Cell.player,
        Cell.none,
        Cell.none,
        Cell.none,
        Cell.none,
        Cell.none,
        Cell.none,
    ]
)
column_player_winner_board_size_3 = board(
    content=[
        Cell.player,
        Cell.none,
        Cell.none,
        Cell.player,
        Cell.none,
        Cell.none,
        Cell.player,
        Cell.none,
        Cell.none,
    ]
)
