from .board import Board

__all__ = (
    'memoize',
)

CACHE: dict[tuple[str, int, bool], int] = {}


def memoize(func):

    def _inner(board: Board, depth: int = 0, is_max: bool = False):
        cache_key = str(board), depth, is_max
        score = CACHE.get(cache_key)
        if score is not None:
            return score
        score = func(board, depth, is_max)
        CACHE[cache_key] = score
        return score

    return _inner
