from ...xo.types import (
    GameMoves,
    XOGame,
)

__all__ = (
    'game_board_response'
)


def game_board_response(game: XOGame, moves: GameMoves) -> dict:
    dict_moves = [
        {
            'row': move.row,
            'column': move.column,
            'player': move.player,
            'created_at': move.created_at,
            'order': move.order,
        }
        for move in moves
    ]
    return {
        'game_id': game.id,
        'user_id': game.user_id,
        'size': game.size,
        'winner': game.winner,
        'created_at': game.created_at,
        'finished_at': game.finished_at,
        'moves': dict_moves,
    }
