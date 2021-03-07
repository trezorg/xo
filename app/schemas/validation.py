__all__ = (
    'auth_schema',
    'start_game_schema',
)

MAX_BOARD_SIZE = 10
MIN_BOARD_SIZE = 3

auth_schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
    },
    'required': ['username', 'password']
}

start_game_schema = {
    'type': 'object',
    'properties': {
        'size': {
            'type': 'integer',
            'default': 3,
            'minimum': MIN_BOARD_SIZE,
            'maximum': MAX_BOARD_SIZE,
        },
    },
    'required': ['size']
}
