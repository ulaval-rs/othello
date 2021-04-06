from typing import Union, List

import geopandas
from numpy import interp

from othello.macbeth.criterion_parameters import CriterionParameters


def evaluate_new_values(series: geopandas.GeoSeries, criterion_parameters: CriterionParameters) -> List:
    # If the levels can be used in a interpolation
    if type(criterion_parameters.levels[0]) in [int, float]:
        x, y = criterion_parameters.levels, criterion_parameters.weights
        new_values = interp(series.values, x, y)

        return [round(value, 2) for value in new_values]

    # If the levels are actually string label
    new_values = []
    for value in series.values:
        index_of_level = criterion_parameters.levels.index(value)
        new_values.append(criterion_parameters.weights[index_of_level])

    return new_values


def cast(value: str) -> Union[str, float, int]:
    """Try to cast str to the corresponding value"""
    try:
        if '.' in value:
            return float(value)

        return int(value)

    except ValueError:
        pass

    return value
