import random
import string
from typing import Optional

import pytest
from flask import url_for

from app.app import create_app
from app.services.user.login import (
    delete_user,
    signup_user,
)
from app.utils import random_string
from app.xo.board import Board
from app.xo.enum import Cell

DEFAULT_BOARD_SIZE = 3


def rand_str(size: int = 10, dictionary: str = string.ascii_lowercase):
    @pytest.fixture
    def _rand():
        def _iter():
            while True:
                yield random_string(size=size, dictionary=dictionary)

        yield _iter()

    return _rand


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.testing = True
    return app


@pytest.fixture
def db_user(app, str_generator):
    username = next(str_generator)
    password = next(str_generator)
    signup_user(app, username, password)
    yield username, password
    delete_user(app, username)


@pytest.fixture
def signup_url():
    return url_for('signup')


@pytest.fixture
def signin_url():
    return url_for('signin')


def board(size: Optional[int] = None, content: Optional[list[Cell]] = None):

    @pytest.fixture
    def _board():
        if content is None and size is None:
            raise ValueError(
                'Wrong function arguments. At least one, '
                'either size or content should be set'
            )
        if content is not None:
            return Board.create(content)
        return Board(size or DEFAULT_BOARD_SIZE)

    return _board


blank_3_board = board(size=3)
left_diagonal_player_winner_board_size_3 = board(
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
right_diagonal_player_winner_board_size_3 = board(
    content=[
        Cell.none,
        Cell.none,
        Cell.player,
        Cell.none,
        Cell.player,
        Cell.none,
        Cell.player,
        Cell.none,
        Cell.none,
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
row_one_step_winner_board_size_3 = board(
    content=[
        Cell.player,
        Cell.player,
        Cell.none,
        Cell.none,
        Cell.computer,
        Cell.none,
        Cell.computer,
        Cell.none,
        Cell.none,
    ]
)
row_one_step_winner_board_size_4 = board(
    content=[
        Cell.none,
        Cell.player,
        Cell.player,
        Cell.player,
        Cell.none,
        Cell.computer,
        Cell.none,
        Cell.none,
        Cell.none,
        Cell.none,
        Cell.computer,
        Cell.none,
        Cell.none,
        Cell.none,
        Cell.none,
        Cell.computer,
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
game_over_no_winner = board(
    content=[
        Cell.player,
        Cell.computer,
        Cell.player,
        Cell.computer,
        Cell.player,
        Cell.computer,
        Cell.computer,
        Cell.player,
        Cell.computer,
    ]
)
str_generator = rand_str()
