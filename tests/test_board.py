from collections import defaultdict

import pytest

from app.xo import (
    Board,
    Cell,
    Winner,
)


def test_left_diagonal_board_winner(left_diagonal_player_winner_board_size_3):
    assert left_diagonal_player_winner_board_size_3.winner == Winner.player


def test_right_diagonal_board_winner(right_diagonal_player_winner_board_size_3):
    assert right_diagonal_player_winner_board_size_3.winner == Winner.player


def test_row_board_winner(row_player_winner_board_size_3):
    assert row_player_winner_board_size_3.winner == Winner.player


def test_column_board_winner(column_player_winner_board_size_3):
    assert column_player_winner_board_size_3.winner == Winner.player


def test_create_board_with_wrong_number_of_elements():
    with pytest.raises(ValueError):
        Board.create([Cell.none, Cell.none, Cell.none])


def test_game_over_no_winner(game_over_no_winner):
    assert not game_over_no_winner._check_rows()
    assert not game_over_no_winner._check_columns()
    assert not game_over_no_winner._check_left_diagonal()
    assert not game_over_no_winner._check_right_diagonal()
    assert not game_over_no_winner._check_diagonals()
    assert game_over_no_winner.winner == Winner.none
    assert game_over_no_winner.is_full
    assert game_over_no_winner.is_over


def test_random_board():
    number = 6
    board = Board.random_board(3, number)
    assert not board.is_full
    cells = defaultdict(int)
    for row in range(board.size):
        for column in range(board.size):
            cells[board.cells[row][column]] += 1
    assert cells[Cell.player] == cells[Cell.computer] == number / 2
