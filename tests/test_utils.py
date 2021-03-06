from itertools import (
    groupby,
    islice,
)

from app.xo.utils import moves_iterable


def test_moves_iterable():
    it = moves_iterable()
    moves = sorted(islice(it, 10))
    grouped_moves = groupby(moves)
    print(grouped_moves)

