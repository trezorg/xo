__all__ = (
    'auth_schema',
    'start_game_schema',
)

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
        },
    },
    'required': ['size']
}
