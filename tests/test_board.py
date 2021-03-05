import pytest

from app.xo import (
    Board,
    Cell,
    Winner,
)


def test_diagonal_board_winner(diagonal_player_winner_board_size_3):
    assert diagonal_player_winner_board_size_3.check_winner() == Winner.player


def test_row_board_winner(row_player_winner_board_size_3):
    assert row_player_winner_board_size_3.check_winner() == Winner.player


def test_column_board_winner(column_player_winner_board_size_3):
    assert column_player_winner_board_size_3.check_winner() == Winner.player


def test_create_board_with_wrong_number_of_elements():
    with pytest.raises(ValueError):
        Board.create([Cell.none, Cell.none, Cell.none])
