from configparser import ConfigParser
from typing import List

from othello.macbeth.criterion_parameters import CriterionParameters
from othello.macbeth.criterion import Criterion


class MacbethParser(ConfigParser):

    def __init__(self, filepath: str, encoding=None) -> None:
        super().__init__()
        self.read(filepath, encoding)

    def get_criteria(self) -> List[Criterion]:
        """
        Data structure in .mcb file:
            Nom1=Global
            Index parent1=0
            Fondamental1=0
            GroupeFondamental1=0
            Expanded1=1
        """
        criteria_section = self['Liste criteres']
        nbr_of_criteria = int(criteria_section['Nombre'])

        criteria = []
        for i in range(1, nbr_of_criteria + 1):
            criteria.append(
                Criterion(
                    name=criteria_section[f'Nom{i}'],
                    parent_index=int(criteria_section[f'Index parent{i}']),
                    fundamental=bool(int(criteria_section[f'Fondamental{i}'])),
                    fundamental_group=bool(int(criteria_section[f'GroupeFondamental{i}'])),
                    expanded=bool(int(criteria_section[f'Expanded{i}']))
                )
            )

        return criteria

    def get_criterion_parameters(self, criterion: Criterion) -> CriterionParameters:
        pass
