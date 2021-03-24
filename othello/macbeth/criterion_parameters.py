from dataclasses import dataclass
from typing import List, Union


@dataclass
class CriterionParameters:
    short_name: str
    nbr_of_levels: int

    levels: List[Union[str, int, float]]
    levels_short: List[Union[str, int, float]]
    levels_orders: List[int]
    normalized_weights: List[float]
    weights: List[float]
