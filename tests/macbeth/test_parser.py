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

    assert len(result) == 9
    assert type(result[0]) == Criterion
    assert result[0].name == 'Connectivité'
    assert result[0].parent_index == 2
    assert result[0].fundamental
    assert not result[0].fundamental_group
    assert not result[0].expanded


def test_get_criterion_parameters(parser: MacbethParser, criterion: Criterion):
    result = parser.get_criterion_parameters(criterion)

    assert type(result) == CriterionParameters
    assert result.short_name == 'Connectivite'
    assert result.nbr_of_levels == 7

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


@pytest.mark.parametrize('criterion_name, expected', [
    ('Rues partagées', Criterion('Rues partagées', 0, False, True, False)),
    ('Dimension sécurité', Criterion('Rues partagées', 0, False, True, False)),
])
def test_find_criterion(parser: MacbethParser, criterion_name: str, expected: Criterion):
    result = parser.find_criterion(criterion_name)

    assert result.name == expected.name


@pytest.mark.parametrize('criterion_name, expected', [
    ('NON-EXISTING-CRITERION', ValueError),
])
def test_find_criterion(parser: MacbethParser, criterion_name: str, expected):
    with pytest.raises(expected):
        parser.find_criterion(criterion_name)


def test_get_weights(parser: MacbethParser):
    result = parser.get_weights()

    assert type(result) == dict
    assert result['Connectivité'] == round(6.92 / 100, 4)
    assert result['Visibilité'] == round(10.77 / 100, 4)
    assert result['Indice canopée'] == round(8.46 / 100, 4)
