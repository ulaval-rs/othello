from dataclasses import dataclass


@dataclass
class Criterion:
    name: str
    parent_index: int
    fundamental: bool
    fundamental_group: bool
    expanded: bool
