
__all__ = (
    'BadRequest',
    'ServerError',
)


class XOExceptions(Exception):

    status_code: int = -1

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(self)
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


class ServerError(XOExceptions):

    status_code = 500
