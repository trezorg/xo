from contextlib import contextmanager
from typing import Type

from sqlalchemy.orm import Session


__all__ = (
    'session_scope',
)


@contextmanager
def session_scope(ses: Type[Session]):
    """Provide a transactional scope around a series of operations."""
    session = ses()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
