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
    assert result[0].name == 'Rues partagées'
    assert result[0].parent_index == 0
    assert not result[0].fundamental
    assert not result[0].fundamental_group
    assert result[0].expanded


def test_get_criterion_parameters(parser: MacbethParser, criterion: Criterion):
    result = parser.get_criterion_parameters(criterion)

    assert type(result) == CriterionParameters
    assert result.short_name == 'Noeud racine'
    assert result.nbr_of_levels == 10

    assert type(result.levels) == list
    assert type(result.levels_short) == list
    assert type(result.levels_orders) == list
    assert type(result.normalized_weights) == list
    assert type(result.weights) == list

    assert type(result.levels[0]) in (str, float, int)
    assert type(result.levels_short[0]) in (str, float, int)
    assert type(result.levels_orders[0]) == int
    assert type(result.normalized_weights[0]) == float
    assert type(result.weights[0]) == float
