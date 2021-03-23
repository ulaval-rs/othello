import pytest

from othello.macbeth.criterion import Criterion
from othello.macbeth.criterion_parameters import CriterionParameters
from othello.macbeth.parser import MacbethParser

MACBETH_FILEPATH = './tests/data/RuesPartagéesSherbrooke.mcb'


@pytest.fixture
def parser():
    return MacbethParser(MACBETH_FILEPATH)


@pytest.fixture
def criterion(parser):
    criteria = parser.get_criteria()

    return criteria[0]


def test_get_criteria(parser: MacbethParser):
    result = parser.get_criteria()

    assert len(result) == 14
    assert type(result[0]) == Criterion


def test_get_criterion_parameters(parser: MacbethParser, criterion: Criterion):
    result = parser.get_criterion_parameters(criterion)

    assert type(result) == CriterionParameters
    assert False
