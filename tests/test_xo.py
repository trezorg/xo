from app.xo.enum import (
    Cell,
    Winner,
)
from app.xo.xo import (
    find_minimax_computer_move,
    find_minimax_player_move,
)


def test_next_player_step_to_win_size3(row_one_step_winner_board_size_3):
    move = find_minimax_player_move(row_one_step_winner_board_size_3)
    row_one_step_winner_board_size_3.set(Cell.player, *move)
    assert row_one_step_winner_board_size_3.winner == Winner.player


def test_next_computer_step_to_win_size3(row_one_step_winner_board_size_3):
    move = find_minimax_computer_move(row_one_step_winner_board_size_3)
    row_one_step_winner_board_size_3.set(Cell.computer, *move)
    assert row_one_step_winner_board_size_3.winner == Winner.computer


def test_next_player_step_to_win_size4(row_one_step_winner_board_size_4):
    move = find_minimax_player_move(row_one_step_winner_board_size_4)
    assert move == (0, 0)
    row_one_step_winner_board_size_4.set(Cell.player, *move)
    assert row_one_step_winner_board_size_4.winner == Winner.player


def test_next_computer_step_to_win_size4(row_one_step_winner_board_size_4):
    move = find_minimax_computer_move(row_one_step_winner_board_size_4)
    assert move == (0, 0)
    row_one_step_winner_board_size_4.set(Cell.computer, *move)
    assert row_one_step_winner_board_size_4.winner == Winner.computer
