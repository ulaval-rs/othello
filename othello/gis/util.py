import copy
import functools
from typing import Dict, List

import pandas
from geopandas import GeoDataFrame

from othello.gis import io


def find_common_columns(dfs: List[GeoDataFrame]) -> List[str]:
    common_columns = functools.reduce(lambda c1, c2: set(c1).intersection(set(c2)), dfs)

    return common_columns


def make_dataframe_with_common_columns(dfs: List[GeoDataFrame], common_columns: List[str]) -> GeoDataFrame:
    df = copy.deepcopy(dfs[0][common_columns])

    return df


def add_weighted_columns_to_dataframe(df: GeoDataFrame, criteria_information: List[Dict], join_on: str) -> GeoDataFrame:
    """Add the weighted criteria to the 'df' dataframe by joining data on the join_on column name.

    Args:
        df: Base GeoDataFrame
        criteria_information: Criteria data that allows to retrieve the exact column from a table from a layer from aGDB file
        join_on: Column name on which the table join will be based

    Returns:
        GeoDataFrame with the added criteria and the final score
    """
    weighted_columns = []

    for criterion_information in criteria_information:
        field = criterion_information['field']
        filepath = criterion_information['filepath']
        layer = criterion_information['layer']
        weight = criterion_information['weight']
        criterion_name = criterion_information['criterion_name']

        criterion_df = io.read(filepath, layer=layer)[[join_on, field]]
        criterion_df.columns = [join_on, criterion_name + '_np']
        criterion_df[criterion_name + '_p'] = weight * criterion_df[criterion_name + '_np']

        df = pandas.merge(left=df, right=criterion_df, on=join_on)
        weighted_columns.append(criterion_name + '_p')

        # df[criterion_name + '_np'] = criterion_df
        # df[criterion_name + '_p'] = weight * criterion_df

    # Final score in a new series
    df['FinalScore'] = [0 for _ in range(len(df))]
    for column in weighted_columns:
        df['FinalScore'] += df[column]

    return df
