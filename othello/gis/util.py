import copy
import functools
from typing import Dict, List

from geopandas import GeoDataFrame

from othello.gis import io


def find_common_columns(dfs: List[GeoDataFrame]) -> List[str]:
    common_columns = functools.reduce(lambda c1, c2: set(c1).intersection(set(c2)), dfs)

    return common_columns


def make_dataframe_with_common_columns(dfs: List[GeoDataFrame], common_columns: List[str]) -> GeoDataFrame:
    df = copy.deepcopy(dfs[0][common_columns])

    return df


def add_weighted_columns_to_dataframe(df: GeoDataFrame, criteria_information: List[Dict]) -> GeoDataFrame:
    weighted_columns = []

    for criterion_information in criteria_information:
        criterion = criterion_information['criterion']
        filepath = criterion_information['filepath']
        layer = criterion_information['layer']
        weight = criterion_information['weight']

        # Removing the _mb suffix
        criterion = criterion.replace('_mb', '')

        criterion_geoseries = io.read(filepath, layer=layer)[criterion]
        df[criterion + '_np'] = criterion_geoseries
        df[criterion + '_p'] = weight * criterion_geoseries
        weighted_columns.append(criterion + '_p')

    # Final score in a new series
    df['FinalScore'] = [0 for _ in range(len(df))]
    for column in weighted_columns:
        df['FinalScore'] += df[column]

    return df