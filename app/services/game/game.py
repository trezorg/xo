import random
from datetime import datetime
from typing import (
    Callable,
    Tuple,
)

from flask import Flask
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ...constant import DEFAULT_GAME_SIZE
from ...exceptions import (
    BadRequest,
    OccupiedCell,
    GameIsOver,
)
from ...models.models import (
    Game,
    Move,
    User,
)
from ...models.session import session_scope
from ...xo.enum import (
    Cell,
    Player,
    Winner,
)
from ...xo.board import Board
from ...xo.types import (
    GameMove,
    GameMoves,
    XOGame,
)
from ...xo.xo import (
    find_minimax_computer_move,
    find_random_move,
)

__all__ = (
    'start_game',
    'store_move',
    'get_moves',
    'delete_game',
)

MINIMAX_MIN_FREE_CELLS = 9


def strategy(board: Board) -> Callable[[Board], tuple[int, int]]:
    """
    Strategy chooses function to calculate next move.
    Until we have more than 9 free cells we will use random choice
    :param board: Board. Game board
    :return: Function to calculate next move
    """
    if board.free_positions_count > MINIMAX_MIN_FREE_CELLS:
        return find_random_move
    return find_minimax_computer_move


def start_game(app: Flask, user: User, size: int = DEFAULT_GAME_SIZE) -> Tuple[XOGame, GameMoves]:
    """
    Start new game with certain board size
    :param app: Flask. Flask application
    :param user: User. sqlalchemy user object
    :param size: int. board size
    :return: (Game, GameMoves). Current game and board state: (Game, GameMoves)
    """
    ses = app.config['session']
    # find player to start game
    start_player = random.choice(list(Player))
    board = Board(size=size)
    computer_started = start_player == Player.computer
    with session_scope(ses) as session:
        game = Game(user_id=user.id, size=size)
        session.add(game)
        session.flush()
        if computer_started:
            row, column = strategy(board)(board)
            position = row * size + column
            store_move(session, game_id=game.id, position=position, player=Player.computer)
        moves = get_moves(session, game_id=game.id, size=size)
        board_game = XOGame(
            id=game.id,
            size=game.size,
            winner=game.winner,
            created_at=game.created_at,
            finished_at=game.finished_at,
            user_id=game.user_id,
        )
    return board_game, moves


def store_move(session: Session, game_id, position: int,
               player: Player, flush=False, commit=False) -> None:
    """
    Create move db record
    :param session: Session. SQLAlchemy session
    :param game_id: int. Game ID
    :param position: int. Board position: row * size + column
    :param player: Player. Game player: [Player.computer, Player.player]
    :param flush: bool. Either flush session
    :param commit: bool. Either commit session
    :return:
    """
    last_order = session.query(func.max(Move.order)).filter(Move.game_id == game_id).scalar()
    last_order = 1 if not last_order else last_order + 1
    move = Move(game_id=game_id, position=position, player=player.value, order=last_order)
    session.add(move)
    if flush:
        session.flush()
    if commit:
        session.commit()


def get_moves(session: Session, game_id, size: int) -> GameMoves:
    """
    Get game moves
    :param session: Session. SQLAlchemy session
    :param game_id: int. Game ID
    :param size: int. Game board size
    :return: GameMoves. Iterator over game moves in order
    """
    moves = session.query(Move).filter(Move.game_id == game_id).order_by(Move.order)
    for move in moves:
        row, column = divmod(move.position, size)
        print(row, column, move.position)
        yield GameMove(
            player=Player(move.player),
            order=move.order,
            row=row,
            column=column,
            created_at=move.created_at
        )


def make_move(app: Flask, user: User, game_id, row, column: int) -> Tuple[int, int]:
    """
    Make player move
    :param app: Flask. Application
    :param user: User. Game user
    :param game_id: int. Game_id
    :param row: int. Board row
    :param column: int. Board column
    :return: tuple[int, int]. Computer turn
    """
    ses = app.config['session']
    with session_scope(ses) as session:
        game = session.query(Game).filter(Game.user_id == user.id, Game.id == game_id).first()
        if game is None:
            raise BadRequest('You do not own this game')
        if row >= game.size:
            raise BadRequest('Row is over the board boundary')
        if column >= game.size:
            raise BadRequest('Column is over the board boundary')
        moves = get_moves(session, game_id, game.size)
        board = Board.from_storage(game.size, moves)
        if board.is_over:
            raise GameIsOver('Game is over')
        if not board.is_free_cell(row, column):
            raise OccupiedCell()
        store_move(session, game_id, row * game.size + column, Player.player)
        board.set(Cell(Player.player.value), row, column)
        if board.is_over:
            game.winner = None if board.winner == Winner.none else board.winner
            game.finished_at = datetime.utcnow()
            session.add(game)
            return -1, -1
        computer_move_row, computer_move_column = strategy(board)(board)
        store_move(
            session,
            game_id,
            computer_move_row * game.size + computer_move_column,
            Player.computer,
        )
        return computer_move_row, computer_move_column


def delete_game(app: Flask, game_id: int):
    """
    Delete the game
    :param app: Flask. Application
    :param game_id: int. Game id
    :return:
    """
    ses = app.config['session']
    with session_scope(ses) as session:
        session.query(Game).filter(Game.id == game_id).delete()
        try:
            session.commit()
        except SQLAlchemyError as err:
            raise BadRequest('Cannot delete game') from err
