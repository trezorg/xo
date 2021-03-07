__all__ = (
    'auth_schema',
    'start_game_schema',
    'move_schema',
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

move_schema = {
    'type': 'object',
    'properties': {
        'row': {
            'type': 'integer',
            'default': 3,
        },
        'column': {
            'type': 'integer',
            'default': 3,
        },
        'game_id': {
            'default': 3,
        },
    },
    'required': ['row', 'column', 'game_id']
}
