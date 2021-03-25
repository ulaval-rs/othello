from typing import Optional

import geopandas


def read(filepath: str, layer: Optional[str] = None) -> geopandas.GeoDataFrame:
    # Use proprietary ESRI driver
    if '.gdb' in filepath.lower():
        if layer is not None:
            return geopandas.read_file(filepath, driver='FileGDB', layer=layer)

        return geopandas.read_file(filepath, driver='FileGDB')

    return geopandas.read_file(filepath)


def write(df: geopandas.GeoDataFrame, filepath: str) -> None:
    if '.gdb' in filepath.lower():
        df.to_file(filepath, driver='FileGDB')

    else:
        df.to_file(filepath)
