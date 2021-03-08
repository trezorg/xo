from typing import Mapping

from jsonschema import validate
from jsonschema.exceptions import ValidationError

__all__ = (
    'auth_schema',
    'start_game_schema',
    'move_schema',
    'page_schema',
    'validate_page_query',
    'DEFAULT_PAGINATION_SIZE'
)

from app.exceptions import BadRequest
from app.utils import (
    is_float,
    is_int,
)

MAX_BOARD_SIZE = 10
MIN_BOARD_SIZE = 3
DEFAULT_PAGE = 1
DEFAULT_PAGINATION_SIZE = 20
MAX_PAGINATION_SIZE = 50

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
            'type': 'integer',
            'default': 1,
        },
    },
    'required': ['row', 'column', 'game_id']
}

page_schema = {
    'type': 'object',
    'properties': {
        'page': {
            'type': 'integer',
            'default': 1,
            'minimum': 1,
        },
        'size': {
            'type': 'integer',
            'default': DEFAULT_PAGINATION_SIZE,
            'maximum': MAX_PAGINATION_SIZE,
        },
    },
}


def validate_page_query(params: Mapping) -> dict:
    dct = {}
    for field in ('page', 'size'):
        if field in params:
            value = params[field]
            if is_int(value) or is_float(value):
                dct[field] = int(value)
            else:
                dct[field] = value
    try:
        validate(dct, page_schema)
    except ValidationError as exc:
        raise BadRequest(exc.message.replace('\n', ', '))
    if 'page' not in dct:
        dct['page'] = DEFAULT_PAGE
    if 'size' not in dct:
        dct['size'] = DEFAULT_PAGINATION_SIZE
    return dct
