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
    Winner,
)
from .board import Board

__all__ = (
    'minimax',
    'find_best_computer_move',
    'find_best_player_move',
)


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

    # If this maximizer's move
    if is_max:
        best = BEST_PLAYER_SCORE
        for row, column in board.blank_positions:
            # Make the move
            board.set(Cell.player, row, column)
            # Call minimax recursively and choose the maximum value
            best = max(best, minimax(board, depth + 1, not is_max))
            board.set(Cell.none, row, column)
        return best

    # If this minimizer's move
    best = BEST_COMPUTER_SCORE
    for row, column in board.blank_positions:
        # Make the move
        board.set(Cell.computer, row, column)
        # Call minimax recursively and choose the minimum value
        best = min(best, minimax(board, depth + 1, not is_max))
        board.set(Cell.none, row, column)
    return best


def find_best_computer_move(board: Board) -> tuple[int, int]:
    """
    Find best move for the computer
    :param board:
    :return: Move as 2-sized tuple
    """
    best = BEST_COMPUTER_SCORE
    best_move = -1, -1

    for row, column in board.blank_positions:
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


def find_best_player_move(board: Board) -> tuple[int, int]:
    """
    Find best move for the player
    :param board:
    :return: Move as 2-sized tuple
    """
    best = BEST_PLAYER_SCORE
    best_move = -1, -1

    for row, column in board.blank_positions:
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
