import os
import shutil

# Fiona need to be imported before geopandas to avoid a current bug
# https://github.com/Toblerity/Fiona/issues/944
import fiona
import geopandas
import pytest

from othello import gis

GDB_FILEPATH = './tests/data/CritereArretsSTS.gdb'
SPH_FILEPATH = './tests/data/stations/stations.shp'
TMP_DIR = './tests/data/tmp'


class TestIO:

    def setup_method(self):
        os.makedirs(TMP_DIR)

    def teardown_method(self):
        shutil.rmtree(TMP_DIR)

    @pytest.mark.parametrize('filepath, layer, expected_nbr_of_columns', [
        (GDB_FILEPATH, None, 35),
        (GDB_FILEPATH, 'ArretsTEST_on_mb', 36),
        (SPH_FILEPATH, None, 5),
    ])
    def test_read(self, filepath, layer, expected_nbr_of_columns):
        result = gis.io.read(filepath, layer)

        assert type(result) == geopandas.GeoDataFrame
        assert len(result.columns) == expected_nbr_of_columns

    @pytest.mark.parametrize('df, filename', [
        (geopandas.read_file(SPH_FILEPATH), os.path.join(TMP_DIR, 'tmp.shp')),
        (geopandas.read_file(GDB_FILEPATH), os.path.join(TMP_DIR, 'tmp.gdb')),
    ])
    def test_write(self, df, filename):
        gis.io.write(df, filename)

        os.path.exists(filename)
        assert self._is_valid_geo_data(filename)

    def _is_valid_geo_data(self, filepath: str) -> bool:
        df = geopandas.read_file(filepath)  # assert file can be read

        return not df.empty
