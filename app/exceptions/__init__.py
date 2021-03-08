
__all__ = (
    'BadRequest',
    'ServerError',
    'GameIsOver',
    'OccupiedCell',
    'XOExceptions'
)


class XOExceptions(Exception):

    status_code: int = -1
    message: str = ""

    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__(self)
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        rv['status_code'] = self.status_code
        if 'description' not in rv:
            rv['description'] = ''
        return rv


class BadRequest(XOExceptions):

    status_code = 400
    message = 'Bad request'


class ServerError(XOExceptions):

    status_code = 500
    message = 'Server error'


class GameIsOver(XOExceptions):

    status_code = 400
    message = 'Game is over'


class OccupiedCell(XOExceptions):

    status_code = 400
    message = 'Cell is already occupied'
