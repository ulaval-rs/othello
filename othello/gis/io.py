import geopandas


def read(filepath: str) -> geopandas.GeoDataFrame:
    # Use proprietary ESRI driver
    if '.gdb' in filepath.lower():
        return geopandas.read_file(filepath, driver='FileGDB')

    return geopandas.read_file(filepath)


def write(df: geopandas.GeoDataFrame, filename: str) -> None:
    df.to_file(filename)
