from typing import Sequence

__all__ = (
    'equal_sequence',
)


def equal_sequence(lst: Sequence) -> bool:
    if not lst:
        return True
    first = lst[0]
    for index in range(1, len(lst)):
        if lst[index] != first:
            return False
    return True
