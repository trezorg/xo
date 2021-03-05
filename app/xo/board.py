import math

from .enum import (
    Cell,
    Winner,
)
from .utils import equal_sequence

BoardType = list[list[Cell]]


class Board:
    size: int
    _board: BoardType

    def __init__(self, size: int = 3):
        if size < 2:
            raise ValueError(f'Board size too small: {size}')
        self._board = [[Cell.none for _ in range(size)] for _ in range(size)]
        self.size = size

    def set(self, cell: Cell, row, column: int):
        self._board[row][column] = cell

    @property
    def is_full(self) -> bool:
        for row in range(self.size):
            for column in range(self.size):
                if self._board[row][column] is Cell.none:
                    return False
        return True

    @classmethod
    def create(cls, data: list[Cell]) -> 'Board':
        size = math.sqrt(len(data))
        if not size.is_integer():
            raise ValueError(f'Wrong size of cell values sequence: {size}')
        size = int(size)
        board = cls(size)
        for index, cell in enumerate(data):
            column, row = divmod(index, size)
            board.set(cell, row, column)
        return board

    def _check_rows(self) -> Winner:
        for row in range(self.size):
            if equal_sequence(self._board[row]):
                return Winner.from_cell(self._board[row][0])
        return Winner.none

    def _check_columns(self) -> Winner:
        for column in range(self.size):
            first = self._board[0][column]
            for row in range(1, self.size):
                if first != self._board[row][column]:
                    break
            return Winner.from_cell(first)
        return Winner.none

    def _check_left_diagonals(self) -> Winner:
        first = self._board[0][0]
        for pos in range(1, self.size):
            if first != self._board[pos][pos]:
                return Winner.none
        return Winner.from_cell(first)

    def _check_right_diagonals(self) -> Winner:
        first = self._board[self.size - 1][self.size - 1]
        for pos in range(self.size - 1, -1, -1):
            if first != self._board[pos][pos]:
                return Winner.none
        return Winner.from_cell(first)

    def _check_diagonals(self) -> Winner:
        return self._check_left_diagonals() or self._check_right_diagonals()

    def check_winner(self) -> Winner:
        return self._check_rows() or self._check_columns() or self._check_diagonals()
