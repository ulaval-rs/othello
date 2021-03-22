import geopandas


def read(filepath: str) -> geopandas.GeoDataFrame:
    # Use proprietary ESRI driver
    if '.gdb' in filepath.lower():
        return geopandas.read_file(filepath, driver='FileGDB')

    return geopandas.read_file(filepath)


def write(df: geopandas.GeoDataFrame, filepath: str) -> None:
    if '.gdb' in filepath.lower():
        df.to_file(filepath, driver='FileGDB')

    else:
        df.to_file(filepath)
