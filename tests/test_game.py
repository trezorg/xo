import random

from app.services.game.game import strategy
from app.xo.board import Board
from app.xo.enum import (
    Cell,
    Player,
    Winner,
)


def test_game():
    board = Board(5)
    player = random.choice(list(Player))
    players = (player, player.opponent)
    start = 0
    while not board.is_over:
        player = players[start % 2]
        start += 1
        move = strategy(board, player=player)(board)
        board.set(Cell(player.value), *move)
    assert board.is_over
    assert board.winner in Winner
