import math
from typing import Iterator

from .enum import (
    Cell,
    Winner,
)
from .utils import (
    equal_sequence,
    moves_generator,
)
from .types import (
    BoardType,
    GameMoves,
    Moves,
    Position,
)


class Board:
    size: int
    _board: BoardType

    def __init__(self, size: int = 3):
        if size < 2:
            raise ValueError(f'Board size too small: {size}')
        self._board: BoardType = [[Cell.none for _ in range(size)] for _ in range(size)]
        self.size: int = size

    def __str__(self):
        result = []
        for row in range(self.size):
            result.append(' '.join(str(c) for c in self._board[row]))
        return '\n'.join(result)

    def set(self, cell: Cell, row, column: int):
        """
        Set a game move for some position
        :param cell: Game cell(move)
        :param row: Row
        :param column: column
        :return: None
        """
        self._board[row][column] = cell

    def is_free_cell(self, row, column: int) -> bool:
        return self._board[row][column] == Cell.none

    @property
    def cells(self) -> BoardType:
        return self._board

    @property
    def is_full(self) -> bool:
        """
        Check either the game board is full
        :return: bool
        """
        for row in range(self.size):
            for column in range(self.size):
                if self._board[row][column] is Cell.none:
                    return False
        return True

    @property
    def free_positions_count(self) -> int:
        """
        Return number of board free positions
        :return: int
        """
        count = 0
        for row in range(self.size):
            for column in range(self.size):
                cell = self._board[row][column]
                if cell is Cell.none:
                    count += 1
        return count

    @property
    def free_positions(self) -> Iterator[Position]:
        """
        Return iterator over blank board cell positions
        :return: Iterator of blank cells
        """
        for row in range(self.size):
            for column in range(self.size):
                cell = self._board[row][column]
                if cell is Cell.none:
                    yield row, column

    @property
    def winner(self) -> Winner:
        """
        Either we have the game winner
        :return: Winner enum
        """
        return self._check_rows() or self._check_columns() or self._check_diagonals()

    @property
    def is_over(self) -> bool:
        """
        Either the game is over
        :return: bool
        """
        return self.is_full or bool(self.winner)

    @classmethod
    def create(cls, data: list[Cell]) -> 'Board':
        """
        Create board from list of cells(moves)
        :param data: List of moves
        :return: Board. Game board
        """
        size = math.sqrt(len(data))
        if not size.is_integer():
            raise ValueError(f'Wrong size of cell values sequence: {size}')
        size = int(size)
        board = cls(size)
        for index, cell in enumerate(data):
            row, column = divmod(index, size)
            board.set(cell, row, column)
        return board

    @classmethod
    def from_moves(cls, size: int, moves: Moves) -> 'Board':
        """
        Construct board from current game movies.
        We need this function to convert list of moves to python board structure.
        :param size: Size of a board
        :param moves: Iterable consists of tuples with 2 elements.
        First positions in tuple is flatten position in board as row * size + column
        Second is an initiator of the move [Cell.player, Cell.computer]
        :return: Game board
        """
        cells = [Cell.none for _ in range(size * size)]
        for move in moves:
            position, initiator = move
            cells[position] = Cell(initiator)
        return cls.create(cells)

    @classmethod
    def from_storage(cls, size: int, moves: GameMoves) -> 'Board':
        """
        Construct board from db records.
        We need this function to convert storage output to python board structure.
        :param size: Size of a board
        :param moves: Iterable consists of db move records.
        :return: Board. Game board
        """
        board = cls(size)
        for move in moves:
            board.set(Cell(move.player), move.row, move.column)
        return board

    @classmethod
    def random_board(cls, size, number: int):
        """
        Generate random board.
        :param size: Board size
        :param number: Number of moves
        :return: Game board
        """
        return cls.from_moves(size, moves_generator(size, number))

    def _check_rows(self) -> Winner:
        """
        Checks either we have winner for rows
        :return: Winner enum
        """
        for row in range(self.size):
            if equal_sequence(self._board[row]):
                return Winner.from_cell(self._board[row][0])
        return Winner.none

    def _check_columns(self) -> Winner:
        """
        Checks either we have winner for columns
        :return: Winner enum
        """
        for column in range(self.size):
            first = self._board[0][column]
            for row in range(1, self.size):
                if first != self._board[row][column]:
                    break
            else:
                return Winner.from_cell(first)
        return Winner.none

    def _check_left_diagonal(self) -> Winner:
        """
        Checks either we have winner for the left diagonal(left upper to right bottom)
        :return: Winner enum
        """
        first = self._board[0][0]
        for pos in range(1, self.size):
            if first != self._board[pos][pos]:
                return Winner.none
        return Winner.from_cell(first)

    def _check_right_diagonal(self) -> Winner:
        """
        Checks either we have winner for the right diagonal(right upper to left bottom)
        :return: Winner enum
        """
        row = 0
        column = self.size - 1
        first = self._board[row][column]
        for index in range(self.size - 1):
            row += 1
            column -= 1
            if first != self._board[row][column]:
                return Winner.none
        return Winner.from_cell(first)

    def _check_diagonals(self) -> Winner:
        """
        Checks either we have winner for any diagonals
        :return:
        """
        return self._check_left_diagonal() or self._check_right_diagonal()
