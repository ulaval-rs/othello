from typing import List

import geopandas
import pytest
from geopandas import GeoDataFrame

from othello import gis

GDB_FILEPATH = './tests/data/CritereArretsSTS.gdb'
SPH_FILEPATH = './tests/data/stations/stations.shp'
TMP_DIR = './tests/data/tmp'


def read_dataframes() -> List[GeoDataFrame]:
    return [
        geopandas.read_file(GDB_FILEPATH, driver='FileGDB', layer='SegAvecInfoArret'),
        geopandas.read_file(GDB_FILEPATH, driver='FileGDB', layer='SegAvecInfoArret_mb'),
        geopandas.read_file(GDB_FILEPATH, driver='FileGDB', layer='ArretsTEST_ON'),
        geopandas.read_file(GDB_FILEPATH, driver='FileGDB', layer='ArretsTEST_ON_mb'),
    ]


class TestUtil:

    @pytest.mark.parametrize('dfs, expected_columns', [
        (read_dataframes(), [
            'NUMEROCIVI',
            'NUMEROCI_1',
            'NUMEROCI_2',
            'NUMEROCI_3',
        ]),
    ])
    def test_find_common_columns(self, dfs, expected_columns):
        result = gis.util.find_common_columns(dfs)

        for column in expected_columns:
            assert column in result

    @pytest.mark.parametrize('dfs, common_columns, expected_columns', [
        (
                read_dataframes(),
                ['NUMEROCIVI', 'NUMEROCI_1', 'NUMEROCI_2', 'NUMEROCI_3'],
                ['NUMEROCIVI', 'NUMEROCI_1', 'NUMEROCI_2', 'NUMEROCI_3']
        ),
    ])
    def test_make_dataframe_with_common_columns(self, dfs, common_columns, expected_columns):
        result = gis.util.make_dataframe_with_common_columns(dfs, common_columns=common_columns)

        assert list(result.columns) == expected_columns

    @pytest.mark.parametrize('df, criteria_info, expected_first_criterion_score, expected_second_criterion_score, expected_first_final_score', [(
            geopandas.read_file(GDB_FILEPATH, driver='FileGDB', layer='ArretsTEST_ON'),
            [{
                'filepath': GDB_FILEPATH,
                'layer': 'ArretsTEST_ON',
                'field': 'NbrArret',
                'weight': .5,
                'criterion_name': 'a-criterion',
            }, {
                'filepath': GDB_FILEPATH,
                'layer': 'ArretsTEST_ON',
                'field': 'NbrArret_mb',
                'weight': .5,
                'criterion_name': 'another-criterion',
            }],
            (1, .5),
            (2, .5),
            8.0,
    )])
    def test_add_weighted_columns_to_dataframe(self, df, criteria_info, expected_first_criterion_score, expected_second_criterion_score, expected_first_final_score):
        result = gis.util.add_weighted_columns_to_dataframe(df, criteria_info)

        assert 'FinalScore' in result.columns
        assert result['a-criteria_np'][0] == expected_first_criterion_score[0]
        assert result['a-criteria_p'][0] == expected_first_criterion_score[1]
        assert result['another-criteria_np'][0] == expected_second_criterion_score[0]
        assert result['another-criteria_p'][0] == expected_second_criterion_score[1]
        assert result['FinalScore'][0] == expected_first_final_score
