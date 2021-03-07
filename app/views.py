import werkzeug
from flasgger import swag_from
from flask import (
    current_app,
    g,
    jsonify,
    make_response,
)
from flask_expects_json import expects_json
from flask_jwt import (
    current_identity,
    jwt_required,
)
from jsonschema import ValidationError

from .schemas.validation import (
    auth_schema,
    start_game_schema,
    move_schema,
)
from .services.game.game import (
    make_move,
    start_game,
)
from .services.game.utils import game_board_response
from .services.user.login import (
    authenticate,
    signup_user,
)


def handle_400_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({
            'error': original_error.message,
            'description': '',
            'status_code': 400
        }), 400)
    elif isinstance(error, werkzeug.exceptions.BadRequest):
        return make_response(jsonify({
            'error': str(error),
            'description': error.description,
            'status_code': error.code
        }), 400)
    error_dict = error.to_dict() if getattr(error, 'to_dict', None) else {
        'error': str(error),
        'status_code': 400,
        'description': '',
    }
    return make_response(jsonify(error_dict), error.status_code)


def handle_exception_request(error):
    return make_response(jsonify(error.to_dict()), error.status_code)


def handle_server_error(error):
    return make_response(jsonify({
        'error': str(error.original_exception),
        'description': error.description,
        'status_code': error.code
    }), 500)


def handle_404_error(error):
    return make_response(jsonify({
        'error': str(error),
        'description': error.description,
        'status_code': error.code
    }), 404)


@expects_json(auth_schema)
@swag_from('swagger/signup.yaml')
def signup():
    data = g.data
    signup_user(current_app, data['username'], data['password'])
    return make_response(jsonify({'success': 'ok'}), 201)


@expects_json(auth_schema)
@swag_from('swagger/signin.yaml')
def signin():
    data = g.data
    user = authenticate(data['username'], data['password'])
    jwt = current_app.config['jwt']
    access_token = jwt.jwt_encode_callback(user)
    resp = make_response(jsonify({"access_token": access_token.decode('utf-8')}), 200)
    resp.headers.extend({'jwt-token': access_token})
    return resp


@jwt_required()
@expects_json(start_game_schema)
@swag_from('swagger/start.yaml')
def start():
    size = g.data['size']
    game, moves = start_game(current_app, current_identity, size)
    response = game_board_response(game, moves)
    return make_response(jsonify(response), 201)


@jwt_required()
@expects_json(move_schema)
@swag_from('swagger/move.yaml')
def move():
    row = g.data['row']
    column = g.data['column']
    game_id = g.data['game_id']
    row, column = make_move(current_app, current_identity, game_id=game_id, row=row, column=column)
    response = {
        'row': row,
        'column': column,
    }
    return make_response(jsonify(response), 201)
