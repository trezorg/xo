import random
from itertools import islice
from typing import (
    Iterable,
    Sequence,
)

__all__ = (
    'equal_sequence',
    'moves_iterable',
    'moves_generator',
)

from .enum import Cell
from .types import (
    Moves,
)


def equal_sequence(lst: Sequence) -> bool:
    """
    Checks if all sequence items are equal
    :param lst: Input sequence
    :return: bool
    """
    if not lst:
        return True
    first = lst[0]
    for index in range(1, len(lst)):
        if lst[index] != first:
            return False
    return True


def moves_iterable() -> Iterable[Cell]:
    cell_moves = Cell.player, Cell.computer
    move_index = random.randrange(0, 2)
    first_move = cell_moves[move_index]
    yield first_move
    while True:
        move_index += 1
        yield cell_moves[move_index % 2]


def moves_generator(size, number: int) -> Moves:
    if size < 2:
        raise ValueError(f'Board size too small: {size}')
    flatten_size = size * size
    if flatten_size < number:
        raise ValueError(
            f'Wrong required motions number. '
            f'Should be less size * size : {size * size}'
        )
    occupied_cells: set[int] = set()
    cells = islice(moves_iterable(), number)
    for cell in cells:
        while True:
            pos = random.randrange(0, flatten_size)
            if pos in occupied_cells:
                continue
            occupied_cells.add(pos)
            yield pos, cell
            break
