from app.xo.enum import (
    Cell,
    Player,
    Winner,
)
from app.xo.xo import (
    find_important_cell,
    find_important_cell_for_computer,
    find_important_column_cells,
    find_important_row_cells,
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


def test_find_important_rows_cell(row_one_step_winner_board_size_3):
    cells, _ = find_important_row_cells(row_one_step_winner_board_size_3, Player.player, defencive=False)
    cells = list(cells)
    assert len(cells) == 1
    assert cells[0] == (0, 2)
    cells, _ = find_important_row_cells(row_one_step_winner_board_size_3, Player.player, defencive=True)
    cells = list(cells)
    assert len(cells) == 4
    possible_positions = ((1, 0), (1, 2), (2, 1), (2, 2))
    for cell in cells:
        assert cell in possible_positions


def test_find_important_column_cell_1(row_one_step_winner_board_size_3):
    cells, _ = find_important_column_cells(row_one_step_winner_board_size_3, Player.player, defencive=False)
    cells = list(cells)
    assert len(cells) == 0
    cells, _ = find_important_column_cells(row_one_step_winner_board_size_3, Player.player, defencive=True)
    cells = list(cells)
    assert len(cells) == 0


def test_find_important_column_cell_2(row_player_winner_board_size_3):
    cells, _ = find_important_column_cells(row_player_winner_board_size_3, Player.player, defencive=False)
    cells = list(cells)
    assert len(cells) == 6
    cells, _ = find_important_column_cells(row_player_winner_board_size_3, Player.player, defencive=True)
    cells = list(cells)
    assert len(cells) == 6


def test_find_important_cell(row_one_step_winner_board_size_3):
    cell = find_important_cell(row_one_step_winner_board_size_3, Player.player, defencive=False)
    assert cell == (0, 2)
    cell = find_important_cell(row_one_step_winner_board_size_3, Player.player, defencive=True)
    assert cell in ((1, 0), (1, 2), (2, 1), (2, 2))


def test_find_important_cell_for_computer_1(row_one_step_winner_board_size_3):
    cell = find_important_cell_for_computer(row_one_step_winner_board_size_3)
    assert cell == (0, 2)


def test_find_important_cell_for_computer_2(game_over_no_winner):
    cell = find_important_cell_for_computer(game_over_no_winner)
    assert cell == (-1, -1)
