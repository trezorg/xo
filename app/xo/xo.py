import random
from collections import defaultdict
from operator import itemgetter
from typing import (
    Callable,
    Iterable,
    Optional,
)

from .constants import (
    BEST_COMPUTER_SCORE,
    BEST_PLAYER_SCORE,
    COMPUTER_SCORE,
    PLAYER_SCORE,
    TIE_SCORE,
)
from .decorator import memoize
from .enum import (
    Cell,
    Diagonal,
    Player,
    Winner,
)
from .board import Board
from .types import Position

__all__ = (
    'minimax',
    'find_minimax_computer_move',
    'find_minimax_player_move',
    'find_first_move',
    'find_random_move',
    'find_important_row_cells',
    'find_important_column_cells',
    'find_important_cell',
    'find_important_cell_for_computer',
    'find_important_cell_for_player',
)

RowColumnItems = list[tuple[Player, int, int]]
DiagonalItems = list[tuple[Player, int, Diagonal]]


@memoize
def minimax(board: Board, depth: int = 0, is_max: bool = False) -> int:
    """
    This is the minimax function. It considers all
    the possible ways the game can go and returns
    the value of the board score
    :param board: Game board
    :param depth: Step in iteration
    :param is_max: Either maximizing score or minimizing (player, computer)
    :return: Best score for game
    """
    winner = board.winner

    if winner == Winner.player:
        return PLAYER_SCORE - depth

    if winner == Winner.computer:
        return COMPUTER_SCORE + depth

    # If there are no more moves and no winner then it is a tie
    if board.is_full:
        return TIE_SCORE

    if is_max:
        best = BEST_PLAYER_SCORE

        for row, column in board.free_positions:
            # Make the move
            board.set(Cell.player, row, column)
            # Call minimax recursively and choose the maximum value
            best = max(best, minimax(board, depth + 1, not is_max))
            board.set(Cell.none, row, column)
        return best

    best = BEST_COMPUTER_SCORE
    for row, column in board.free_positions:
        # Make the move
        board.set(Cell.computer, row, column)
        # Call minimax recursively and choose the minimum value
        best = min(best, minimax(board, depth + 1, not is_max))
        board.set(Cell.none, row, column)
    return best


def find_minimax_computer_move(board: Board) -> Position:
    """
    Find best move for the computer
    :param board: Board. Game board
    :return: Position. Move as 2-sized tuple
    """
    best = BEST_COMPUTER_SCORE
    best_move = -1, -1

    for row, column in board.free_positions:
        # Make the move
        board.set(Cell.computer, row, column)

        # compute evaluation function for this move.
        move = minimax(board, 0, False)

        # Undo the move
        board.set(Cell.none, row, column)

        if move < best:
            best_move = row, column
            best = move

    return best_move


def find_minimax_player_move(board: Board) -> Position:
    """
    Find best move for the player
    :param board: Board. Game board
    :return: Position. Move as 2-sized tuple
    """
    best = BEST_PLAYER_SCORE
    best_move = -1, -1

    for row, column in board.free_positions:
        # Make the move
        board.set(Cell.player, row, column)

        # compute evaluation function for this move.
        move = minimax(board, 0, True)

        # Undo the move
        board.set(Cell.none, row, column)

        if move > best:
            best_move = row, column
            best = move

    return best_move


def find_first_move(board: Board) -> Position:
    """
    Find first free cell
    :param board:
    :return: Position. Move as 2-sized tuple
    """
    if board.is_over:
        return -1, -1
    return next(board.free_positions)


def find_random_move(board: Board) -> Position:
    """
    Find random free cell
    :param board:
    :return: Position. Move as 2-sized tuple
    """
    if board.is_over:
        return -1, -1
    return random.choice(list(board.free_positions))


def _get_comparator(player: Player, defencive: bool = True) -> Callable[[tuple[Player, int, int]], tuple[int, int]]:

    if defencive:

        def comp(value):  # type: ignore
            # opponent first. disturb the player
            return int(value[0] != player), value[1]

        return comp

    def comp(value):  # type: ignore
        # player first. Try to win
        return int(value[0] == player), value[1]

    return comp


def _find_maximum_items(items: RowColumnItems, player: Player, defencive: bool) -> tuple[list[int], int]:
    comparator = _get_comparator(player, defencive)
    s_items = sorted(items, key=comparator, reverse=True)
    max_item = s_items[0][-1]
    number = s_items[0][1]
    max_items = [max_item]
    for i in range(1, len(s_items)):
        rec = s_items[i]
        if number == rec[1]:
            max_items.append(rec[-1])
    return max_items, number


def _sort_row_items(board: Board, items: RowColumnItems,
                    player: Player, defencive: bool) -> tuple[Iterable[Position], int]:

    max_items, number = _find_maximum_items(items, player, defencive)

    it = (
        (row_index, column_index)
        for row_index in max_items
        for column_index, cell in enumerate(board.cells[row_index]) if cell.is_none
    )
    return it, number


def _sort_column_items(board: Board, items: RowColumnItems,
                       player: Player, defencive: bool) -> tuple[Iterable[Position], int]:

    max_items, number = _find_maximum_items(items, player, defencive)

    it = ((row_index, column_index)
          for column_index in max_items
          for row_index, row in enumerate(board.cells) if row[column_index].is_none)
    return it, number


def _sort_diagonals_items(board: Board, items: DiagonalItems,
                          player: Player, defencive: bool) -> tuple[Iterable[Position], int]:

    comparator = _get_comparator(player, defencive)
    s_items = sorted(items, key=comparator, reverse=True)

    number = s_items[0][1]
    diagonal = s_items[0][-1]
    diagonals = [diagonal]

    for i in range(1, len(s_items)):
        rec = s_items[i]
        if number == rec[1]:
            diagonals.append(rec[-1])

    diagonals = list(set(diagonals))

    result: list[Position] = []

    for diagonal in diagonals:
        if diagonal.is_left:
            result.extend(((pos, pos) for pos in range(board.size) if board.cells[pos][pos].is_none))
        else:
            row = 0
            column = board.size - 1
            for _ in range(board.size - 1):
                cell = board.cells[row][column]
                if cell.is_none:
                    result.append((row, column))
                row += 1
                column -= 1

    return result, number


def find_important_row_cells(board: Board, player: Player, defencive: bool = True) -> tuple[Iterable[Position], int]:
    """
    Find either best turn fo ourselves, rows without opponent turns, or prevent the opponent to win
    rows without our turns
    :param board: Board. Game board
    :param player: Player
    :param defencive: bool. Strategy. Either we maximize own income or we prevent the opponent to win
    :return: Iterable of board position
    """
    items: list[tuple[Player, int, int]] = []
    for row_index in range(board.size):
        row = board.cells[row_index]
        row_dict: dict[Cell, int] = defaultdict(int)
        for cell in row:
            if cell.is_none:
                continue
            row_dict[cell] += 1
        # if both players made turns on this row it never wins
        if len(row_dict) == 2:
            continue
        for cell, number in row_dict.items():
            items.append((Player(cell.value), number, row_index))
            break

    if not items:
        return iter(()), 0

    return _sort_row_items(board, items, player, defencive)


def find_important_column_cells(board: Board,
                                player: Player, defencive: bool = True) -> tuple[Iterable[Position], int]:
    """
    Find either best turn fo ourselves, columns without opponent turns, or prevent the opponent to win,
    columns without our turns
    :param board: Board. Game board
    :param player: Player
    :param defencive: bool. Strategy. Either we maximize own income or we prevent the opponent to win
    :return: Iterable of board position
    """
    items: list[tuple[Player, int, int]] = []
    for column_index in range(board.size):
        column_dict: dict[Cell, int] = defaultdict(int)
        for row_index in range(board.size):
            cell = board.cells[row_index][column_index]
            if cell.is_none:
                continue
            column_dict[cell] += 1
        # if both players made turns on this column it never wins
        if len(column_dict) == 2:
            continue
        for cell, number in column_dict.items():
            items.append((Player(cell.value), number, column_index))
            break

    if not items:
        return iter(()), 0

    return _sort_column_items(board, items, player, defencive)


def find_important_diagonal_cells(board: Board,
                                  player: Player, defencive: bool = True) -> tuple[Iterable[Position], int]:
    """
    Find either best turn fo ourselves, diagonals without opponent turns, or prevent the opponent to win,
    diagonals without our turns
    :param board: Board. Game board
    :param player: Player
    :param defencive: bool. Strategy. Either we maximize own income or we prevent the opponent to win
    :return: Iterable of board position
    """
    items: DiagonalItems = []
    diagonal_dict: dict[Cell, int] = defaultdict(int)

    # left diagonal
    for pos in range(board.size):
        cell = board.cells[pos][pos]
        if cell.is_none:
            continue
        diagonal_dict[cell] += 1

    # if both players made turns on this column it never wins
    if len(diagonal_dict) == 1:
        for cell, number in diagonal_dict.items():
            items.append((Player(cell.value), number, Diagonal.left))
            break

    diagonal_dict.clear()

    # right diagonal
    row = 0
    column = board.size - 1
    for _ in range(board.size - 1):
        cell = board.cells[row][column]
        if cell.is_none:
            continue
        diagonal_dict[cell] += 1
        row += 1
        column -= 1

    # if both players made turns on this column it never wins
    if len(diagonal_dict) == 1:
        for cell, number in diagonal_dict.items():
            items.append((Player(cell.value), number, Diagonal.right))
            break

    if not items:
        return iter(()), 0

    return _sort_diagonals_items(board, items, player, defencive)


def find_important_cell(board: Board, player: Player, defencive: bool = True) -> Optional[Position]:

    row_cells, row_number = find_important_row_cells(board, player, defencive)
    column_cells, column_number = find_important_column_cells(board, player, defencive)
    diagonal_cells, diagonal_number = find_important_diagonal_cells(board, player, defencive)
    row_cells = set(row_cells)
    column_cells = set(column_cells)
    diagonal_cells = set(diagonal_cells)

    cells = row_cells, column_cells, diagonal_cells

    if not any(cells):
        return None

    all_common_cells = row_cells & column_cells & diagonal_cells
    if all_common_cells:
        return all_common_cells.pop()

    # find max crossing cells (rows, columns, diagonals)

    crossing = 0
    pair = None

    for first in range(len(cells)):
        for second in range(first + 1, len(cells)):
            new_pair = cells[first] & cells[second]
            if len(new_pair) > crossing:
                pair = new_pair

    if pair is not None:
        return pair.pop()

    # return some direction that most populated. Either rows, columns or diagonals
    most_populated_cells, _ = sorted(
        zip(cells, (row_number, column_number, diagonal_number)),
        key=itemgetter(1),
        reverse=True
    )[0]
    if not most_populated_cells:
        return None
    return most_populated_cells.pop()


def find_important_cell_for_computer(board: Board) -> Position:
    cell = find_important_cell(board, Player.computer, True)
    if cell is None:
        return find_random_move(board)
    return cell


def find_important_cell_for_player(board: Board) -> Position:
    cell = find_important_cell(board, Player.player, True)
    if cell is None:
        return find_random_move(board)
    return cell
