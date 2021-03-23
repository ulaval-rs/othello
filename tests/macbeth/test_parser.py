import pytest

from othello.macbeth.criterion import Criterion
from othello.macbeth.parser import MacbethParser

MACBETH_FILEPATH = './tests/data/RuesPartagéesSherbrooke.mcb'


@pytest.fixture
def parser() -> MacbethParser:
    return MacbethParser(MACBETH_FILEPATH)


def test_criteria(parser: MacbethParser):
    result = parser.get_criteria()

    assert len(result) == 14
    assert type(result[0]) == Criterion
