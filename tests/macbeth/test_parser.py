import pytest

from othello.macbeth.parser import MacbethParser

MACBETH_FILEPATH = './tests/data/RuesPartagéesSherbrooke.mcb'


@pytest.fixture
def parser():
    return MacbethParser(MACBETH_FILEPATH)
