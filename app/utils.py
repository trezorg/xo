import random
import string

__all__ = (
    'random_string',
)


def random_string(size: int = 10, dictionary: str = string.ascii_lowercase):
    return ''.join(random.choice(dictionary) for _ in range(size))
