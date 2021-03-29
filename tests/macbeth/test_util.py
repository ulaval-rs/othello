import geopandas
import pytest

from othello.macbeth.criterion_parameters import CriterionParameters
from othello.macbeth.parser import MacbethParser
from othello.macbeth.util import cast, evaluate_new_values

GDB_FILEPATH = './tests/data/CritereArretsSTS.gdb'
MACBETH_FILEPATH = './tests/data/RuesPartagéesSherbrooke.mcb'


def make_criterion_parameters():
    parser = MacbethParser(MACBETH_FILEPATH)
    criteria = parser.get_criteria()

    return parser.get_criterion_parameters(criteria[12])


@pytest.mark.parametrize('series, criterion_parameters', [
    (geopandas.read_file(GDB_FILEPATH, layer='ArretsTEST_ON')['NbrArret'], make_criterion_parameters()),
])
def test_evaluate_new_values(series: geopandas.GeoSeries, criterion_parameters: CriterionParameters):
    result = evaluate_new_values(series, criterion_parameters)

    assert type(result) == list
    assert len(result) == len(series)


@pytest.mark.parametrize('value, expected_value, expected_type', [
    ('a_str', 'a_str', str),
    ('1', 1, int),
    ('1.1', 1.1, float),
])
def test_cast(value, expected_value, expected_type):
    result = cast(value)

    assert result == expected_value
    assert type(result) == expected_type

