import pytest

from app.exceptions import BadRequest
from app.schemas.validation import (
    DEFAULT_PAGINATION_SIZE,
    validate_page_query,
)


def test_validate_page_query():
    result = validate_page_query({'page': '1'})
    assert result['page'] == 1
    assert result['size'] == DEFAULT_PAGINATION_SIZE


def test_validate_page_query_wrong_request():
    with pytest.raises(BadRequest):
        validate_page_query({'page': '-1'})
    with pytest.raises(BadRequest):
        validate_page_query({'page': 'a'})
