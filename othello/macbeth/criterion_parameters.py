from dataclasses import dataclass
from typing import List


@dataclass
class CriterionParameters:
    short_name: str
    nbr_of_levels: int

    levels: List[str]
    levels_short: List[str]
    levels_orders: List[int]
    normalized_weights: List[float]
    weights: List[float]
