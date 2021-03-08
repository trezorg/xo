from ...xo.types import (
    GameMoves,
    XOGame,
)

__all__ = (
    'game_board_response'
)


def game_board_response(game: XOGame, moves: GameMoves) -> dict:
    dict_moves = [move.to_dict() for move in moves]
    dict_game = game.to_dict()
    dict_game['moves'] = dict_moves
    return dict_game
