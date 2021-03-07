from flask import (
    Flask,
    current_app,
)
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy.exc import (
    IntegrityError,
    SQLAlchemyError,
)

from app.exceptions import (
    BadRequest,
)
from app.models.models import User
from app.models.session import session_scope

__all__ = (
    'signup_user',
    'authenticate',
    'delete_user',
    'identity',
)


def signup_user(app: Flask, username, password: str) -> User:
    hashed = pbkdf2_sha256.hash(password)
    ses = app.config['session']
    with session_scope(ses) as session:
        user = User(login=username, password=hashed)
        session.add(user)
        try:
            session.commit()
        except IntegrityError as err:
            raise BadRequest('Login already exists') from err
    return user


def delete_user(app: Flask, username: str):
    ses = app.config['session']
    with session_scope(ses) as session:
        session.query(User).filter(User.login == username).delete()
        try:
            session.commit()
        except SQLAlchemyError as err:
            raise BadRequest('Cannot delete user') from err


def authenticate(username, password: str):
    ses = current_app.config['session']
    with session_scope(ses) as session:
        user = session.query(User).filter(User.login == username).first()
        if user is None:
            raise BadRequest('User does not exist')
        if not pbkdf2_sha256.verify(password, user.password):
            raise BadRequest('Password does not match')
        return user


def identity(payload):
    user_id = payload['identity']
    ses = current_app.config['session']
    with session_scope(ses) as session:
        user = session.query(User).filter(User.id == user_id).scalar()
        return user
