from itertools import (
    groupby,
    islice,
)

from app.xo.utils import moves_iterable


def test_moves_iterable():
    it = moves_iterable()
    number = 100
    moves = sorted(islice(it, number))
    grouped_moves = groupby(moves)
    for group, it in grouped_moves:
        assert len(list(it)) == number / 2
