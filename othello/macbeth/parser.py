from configparser import ConfigParser
from typing import List

from othello.macbeth.criterion_parameters import CriterionParameters
from othello.macbeth.criterion import Criterion
from othello.macbeth.util import cast


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
        """
        Data structure in .mcb file:
            NomCourt=Noeud racine
            ...
            Nombre niveaux=12
            ...
            Niv1=[ toutes références inférieures ]
            |
            Niv12=Réseau de transport collectif
            Niv1short=[ toutes inf ]
            |
            Niv12short=[ RTC ]
            Perm(1)=7
            |
            Perm(12)=1
            ....
            EchelleCourante1=0.00
            |
            EchelleCourante12=2.50
        """
        parameters_section = self[f"Parametres du critere {criterion.name}"]
        short_name = parameters_section['NomCourt']
        nbr_of_levels = int(parameters_section['Nombre niveaux'])

        levels = []
        levels_short = []
        levels_orders = []
        normalized_weights = []
        weights = []

        for i in range(1, nbr_of_levels + 1):
            levels.append(cast(parameters_section[f'Niv{i}']))
            levels_short.append(cast(parameters_section[f'Niv{i}Short']))
            levels_orders.append(int(parameters_section[f'Perm({i})']))
            normalized_weights.append(float(parameters_section[f'EchelleMacbeth{i}']))
            weights.append(float(parameters_section[f'EchelleCourante{i}']))

        return CriterionParameters(
            short_name=short_name,
            nbr_of_levels=nbr_of_levels,
            levels=levels,
            levels_short=levels_short,
            levels_orders=levels_orders,
            normalized_weights=normalized_weights,
            weights=weights,
        )

    def find_criterion(self, criterion_name: str) -> Criterion:
        for criterion in self.get_criteria():
            if criterion.name == criterion_name:
                return criterion

        raise ValueError('Criterion not found')
