import os
import string
from datetime import timedelta
from distutils.util import strtobool

from flasgger import Swagger
from flask import Flask
from flask_jwt import JWT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .exceptions import XOExceptions
from .services.user.login import (
    authenticate,
    identity,
)
from .utils import random_string
from .views import (
    game,
    games,
    handle_400_request,
    handle_404_error,
    handle_exception_request,
    handle_server_error,
    move,
    signin,
    signup,
    start,
)
from .constant import (
    DEFAULT_POSTGRESQL_URI,
    JWT_EXPIRATION_DELTA,
)


def create_app():
    """
    Prepare flask application
    :return: Flask application
    """
    app = Flask(__name__)
    secret_key = os.getenv('SECRET_KEY')
    if secret_key is None:
        secret_key = random_string(size=20, dictionary=string.printable)
    app.config['SECRET_KEY'] = secret_key
    debug = strtobool(os.getenv('DEBUG', 'False'))
    app.debug = debug
    postgresql_url = os.getenv('POSTGRESQL_URL', DEFAULT_POSTGRESQL_URI)
    jwt_expiration = os.getenv('JWT_EXPIRATION_DELTA', JWT_EXPIRATION_DELTA)
    engine = create_engine(postgresql_url, echo=False)
    session = sessionmaker(bind=engine, expire_on_commit=False)
    app.config['session'] = session
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=jwt_expiration)
    app.config['SWAGGER'] = {}
    app.config['SWAGGER']['openapi'] = '3.0.2'
    Swagger(
        app=app,
        template={
            "securityDefinitions": {
                "APIKeyHeader": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header"
                }
            },
            "info": {
                "title": "XO Swagger",
                "version": "1.0",
            },
            "consumes": [
                "application/json",
            ],
            "produces": [
                "application/json",
            ],
        },
    )

    app.errorhandler(400)(handle_400_request)
    app.errorhandler(XOExceptions)(handle_exception_request)
    app.errorhandler(500)(handle_server_error)
    app.errorhandler(404)(handle_404_error)
    app.route('/signup', methods=['POST'])(signup)
    app.route('/signin', methods=['POST'])(signin)
    app.route('/start', methods=['POST'])(start)
    app.route('/move', methods=['POST'])(move)
    app.route('/games', methods=['GET'])(games)
    app.route('/game/<int:game_id>', methods=['GET'])(game)

    jwt = JWT(app, authenticate, identity)
    app.config['jwt'] = jwt
    app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
    return app
