from configparser import ConfigParser
from typing import List

from othello.macbeth.criterion import Criterion


class MacbethParser(ConfigParser):

    def __init__(self, filepath: str, encoding=None) -> None:
        super().__init__()
        self.read(filepath, encoding)

    def get_criteria(self) -> List[Criterion]:
        criteria_section = self['Liste criteres']
        nbr_of_criteria = int(criteria_section['Nombre'])

        criteria = []
        for i in range(1, nbr_of_criteria + 1):
            criteria.append(
                Criterion(
                    name=criteria_section[f'Nom{i}'],
                    parent_index=int(criteria_section[f'Index parent{i}']),
                    fundamental=bool(criteria_section[f'Fondamental{i}']),
                    fundamental_group=bool(criteria_section[f'GroupeFondamental{i}']),
                    expanded=bool(criteria_section[f'Expanded{i}'])
                )
            )

        return criteria
