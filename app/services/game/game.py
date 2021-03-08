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
    Forbidden,
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
)
from ...xo.board import Board
from ...xo.types import (
    GameMove,
    GameMoves,
    Position,
    XOGame,
    XOGames,
)
from ...xo.xo import (
    find_important_cell_for_computer,
    find_important_cell_for_player,
    find_minimax_computer_move,
    find_minimax_player_move,
)

__all__ = (
    'start_game',
    'store_move',
    'get_moves',
    'get_games',
    'get_game',
    'make_move',
    'delete_game',
    'strategy',
)

MINIMAX_MIN_FREE_CELLS = 9


def strategy(board: Board, player: Player = Player.computer) -> Callable[[Board], Position]:
    """
    Strategy chooses function to calculate next move.
    Until we have more than 9 free cells we will use custom function with random choice fallback
    We use the minimax algorithm in case we have 9 and less free cells
    :param player: Player. Player for this turn
    :param board: Board. Game board
    :return: Function to calculate next move
    """
    if board.free_positions_count > MINIMAX_MIN_FREE_CELLS:
        return find_important_cell_for_computer if player.is_computer else find_important_cell_for_player
    return find_minimax_computer_move if player.is_computer else find_minimax_player_move


def start_game(app: Flask, user: User, size: int = DEFAULT_GAME_SIZE) -> Tuple[XOGame, GameMoves]:
    """
    Start new game with certain board size
    :param app: Flask. Flask application
    :param user: User. sqlalchemy user object
    :param size: int. board size
    :return: (XOGame, GameMoves). Current game and board state
    """
    ses = app.config['session']
    # find player to start game
    start_player = random.choice(list(Player))
    computer_started = start_player == Player.computer
    with session_scope(ses) as session:
        game = Game(user_id=user.id, size=size)
        session.add(game)
        session.flush()
        if computer_started:
            # put right to the center of the board for the first turn
            center = size // 2
            row, column = center, center
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


def get_game(app: Flask, user: User, game_id: int) -> Tuple[XOGame, GameMoves]:
    """
    Get game by id
    :param app: Flask. Application
    :param game_id: int
    :param user: User
    :return: (XOGame, GameMoves). Current game and board state
    """
    ses = app.config['session']
    with session_scope(ses) as session:
        game = session.query(Game).filter(Game.user_id == user.id, Game.id == game_id).first()
        if game is None:
            raise Forbidden('You do not own this game')
        moves = get_moves(session, game_id=game.id, size=game.size)
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
    :param flush: bool. Flush session
    :param commit: bool. Commit session
    :return:
    """
    last_order = session.query(func.coalesce(func.max(Move.order), 1)).filter(Move.game_id == game_id).scalar()
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
        yield GameMove(
            player=Player(move.player),
            order=move.order,
            row=row,
            column=column,
            created_at=move.created_at
        )


def _finish_game(session: Session, game: Game, board: Board) -> tuple[int, int]:
    game.winner = board.winner or None
    game.finished_at = datetime.utcnow()
    session.add(game)
    return -1, -1


def make_move(app: Flask, user: User, game_id, row, column: int) -> Tuple[int, int]:
    """
    Make player move
    :param app: Flask. Application
    :param user: User. Game user
    :param game_id: int. Game_id
    :param row: int. Board row
    :param column: int. Board column
    :return: Position. Computer turn
    """
    ses = app.config['session']
    with session_scope(ses) as session:
        game = session.query(Game).filter(Game.user_id == user.id, Game.id == game_id).first()
        if game is None:
            raise BadRequest('You do not own this game')
        if row >= game.size or row < 0:
            raise BadRequest('Row is over the board boundary')
        if column >= game.size or column < 0:
            raise BadRequest('Column is over the board boundary')

        moves = get_moves(session, game_id, game.size)
        board = Board.from_storage(game.size, moves)

        if board.is_over:
            raise GameIsOver('Game is over')
        if not board.is_free_cell(row, column):
            raise OccupiedCell()

        position = row * game.size + column
        store_move(session, game_id, position, Player.player)
        board.set(Cell(Player.player.value), row, column)
        if board.is_over:
            return _finish_game(session, game, board)

        computer_move_row, computer_move_column = strategy(board)(board)
        board.set(Cell(Player.computer.value), computer_move_row, computer_move_column)
        position = computer_move_row * game.size + computer_move_column
        store_move(session, game_id, position, Player.computer)
        if board.is_over:
            return _finish_game(session, game, board)

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


def get_games(app: Flask, user: User, page, size: int) -> tuple[XOGames, int]:
    """
    List of games for user
    :param app: Flask. Application
    :param user: User
    :param page: int
    :param size: int
    :return: XOGames. List of games
    """
    ses = app.config['session']
    offset = (page - 1) * size
    with session_scope(ses) as session:
        games = session.query(Game).filter(Game.user_id == user.id).\
            order_by(Game.created_at.desc()).offset(offset).limit(size)
        total_games = session.query(Game).filter(Game.user_id == user.id).count()
        it = (XOGame(
            id=game.id,
            user_id=user.id,
            size=game.size,
            winner=game.winner,
            created_at=game.created_at,
            finished_at=game.finished_at,
        ) for game in games)
        return it, total_games
