import pytest

from othello.macbeth.util import cast


@pytest.mark.parametrize('value, expected_value, expected_type', [
    ('a_str', 'a_str', str),
    ('1', 1, int),
    ('1.1', 1.1, float),
])
def test_cast(value, expected_value, expected_type):
    result = cast(value)

    assert result == expected_value
    assert type(result) == expected_type
