from typing import List

# Fiona need to be imported before geopandas to avoid a current bug
# https://github.com/Toblerity/Fiona/issues/944
import fiona
import geopandas
import pytest

from othello.macbeth.criterion_parameters import CriterionParameters
from othello.macbeth.parser import MacbethParser
from othello.macbeth.util import cast, evaluate_new_values

GDB_FILEPATH = './tests/data/CritereArretsSTS.gdb'
MACBETH_FILEPATH = './tests/data/RuesPartagéesSherbrooke.mcb'


def make_criterion_parameters(criterion: str):
    parser = MacbethParser(MACBETH_FILEPATH)
    criteria = parser.get_criteria()

    if criterion == 'arrets':
        return parser.get_criterion_parameters(criteria[7])

    if criterion == 'canopee':
        return parser.get_criterion_parameters(criteria[2])

    if criterion == 'defavorise':
        return parser.get_criterion_parameters(criteria[5])

    raise ValueError('Criterion not found')


@pytest.mark.parametrize('series_values, criterion_parameters, use_indexes, expected_first_value', [
    (geopandas.read_file(GDB_FILEPATH, layer='ArretsTEST_ON')['NbrArret'].values, make_criterion_parameters('arrets'), False, -46.67),
    ([15], make_criterion_parameters('arrets'), False, 50.0),
    (['15%'], make_criterion_parameters('canopee'), False, 225.0),
    ([2], make_criterion_parameters('defavorise'), True, -65.0),
])
def test_evaluate_new_values(series_values: List, criterion_parameters: CriterionParameters, use_indexes, expected_first_value):
    result = evaluate_new_values(series_values, criterion_parameters, use_indexes)

    assert type(result) == list
    assert len(result) == len(series_values)
    assert result[0] == expected_first_value


@pytest.mark.parametrize('value, expected_value, expected_type', [
    ('a_str', 'a_str', str),
    ('1', 1, int),
    ('1.1', 1.1, float),
])
def test_cast(value, expected_value, expected_type):
    result = cast(value)

    assert result == expected_value
    assert type(result) == expected_type

