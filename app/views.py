import werkzeug
from flasgger import swag_from
from flask import (
    current_app,
    g,
    jsonify,
    make_response,
)
from flask_expects_json import expects_json
from jsonschema import ValidationError

from .schemas.signup import (
    auth_schema,
    # start_game_schema,
)
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


def handle_bad_request(error):
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
@swag_from('schemas/signup.yaml')
def signup():
    data = g.data
    signup_user(current_app, data['username'], data['password'])
    return jsonify({'success': 'ok'})


@expects_json(auth_schema)
@swag_from('schemas/signin.yaml')
def signin():
    data = g.data
    user = authenticate(data['username'], data['password'])
    jwt = current_app.config['jwt']
    access_token = jwt.jwt_encode_callback(user)
    resp = make_response(jsonify({"access_token": access_token.decode('utf-8')}), 200)
    resp.headers.extend({'jwt-token': access_token})
    return resp


'''
@expects_json(start_game_schema)
@swag_from('schemas/signin.yaml')
def start():
    size = g.data['size']
    user = authenticate(data['username'], data['password'])
    jwt = current_app.config['jwt']
    access_token = jwt.jwt_encode_callback(user)
    resp = make_response(jsonify({"access_token": access_token.decode('utf-8')}), 200)
    resp.headers.extend({'jwt-token': access_token})
    return resp
'''
