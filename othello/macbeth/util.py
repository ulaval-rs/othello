from typing import Union, List

import geopandas
import numpy

from othello.macbeth.criterion_parameters import CriterionParameters


def evaluate_new_values(x_to_eval: List[Union[float, int, str]], criterion_parameters: CriterionParameters) -> List:
    # If the levels can be used in a interpolation
    if type(criterion_parameters.levels[0]) in [int, float]:
        x, y = numpy.array(criterion_parameters.levels), numpy.array(criterion_parameters.weights)
        # x must be sort in order to work with the interp function
        sorted_indexes = numpy.argsort(x)
        x, y = x[sorted_indexes], y[sorted_indexes]

        new_values = numpy.interp(x_to_eval, x, y)

        return [round(value, 2) for value in new_values]

    # If the levels are string label
    new_values = []
    for value in x_to_eval:
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
