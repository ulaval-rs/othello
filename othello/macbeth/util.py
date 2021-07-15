from typing import Union, List

import numpy

from othello.macbeth.criterion_parameters import CriterionParameters


def evaluate_new_values(
        x_to_eval_or_indexes: List[Union[float, int, str]],
        criterion_parameters: CriterionParameters,
        use_indexes: bool = False) -> List:
    # If using indexes (counting from 1) in the macbeth file rather than raw values
    if use_indexes:
        new_values = []
        return [criterion_parameters.weights[i-1] for i in x_to_eval_or_indexes]

    # If the levels can be used in a interpolation
    if type(criterion_parameters.levels[0]) in [int, float]:
        x, y = numpy.array(criterion_parameters.levels), numpy.array(criterion_parameters.weights)
        # x must be sort in order to work with the interp function
        sorted_indexes = numpy.argsort(x)
        x, y = x[sorted_indexes], y[sorted_indexes]

        new_values = numpy.interp(x_to_eval_or_indexes, x, y)

        return [round(value, 2) for value in new_values]

    # If the levels are string label
    new_values = []
    for x in x_to_eval_or_indexes:
        index_of_level = criterion_parameters.levels.index(x)
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
