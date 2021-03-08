import random
import string

__all__ = (
    'random_string',
    'is_int',
    'is_float',
)


def random_string(size: int = 10, dictionary: str = string.ascii_lowercase):
    return ''.join(random.choice(dictionary) for _ in range(size))


def is_int(n):
    try:
        float_n = float(n)
        int_n = int(float_n)
    except ValueError:
        return False
    else:
        return float_n == int_n


def is_float(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return True
