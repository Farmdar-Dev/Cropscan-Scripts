import geopandas as gpd


def build_dataframe(filepaths: list):
    """
    Converts file paths into dataframes

    Args:
        filepaths (list): _description_
    """
    return [gpd.read_file(file) for file in filepaths]


def validate_dataframe():
    pass


def reproject_df_crs(dataframe, crs=None):
    """
    Reprojects the dataframe to the specified CRS
    if no CRS is specified, it will estimate the utm CRS
    """
    if crs is None:
        crs = dataframe.estimate_utm_crs()
    dataframe.to_crs(crs, inplace=True)
    pass


def reproject_dfs_crs(dataframes: list, crs=None):
    """
    Reprojects the list of dataframe to the specified CRS
    if no CRS is specified, it will estimate the utm CRS
    """
    [reproject_df_crs(df, crs) for df in dataframes]


if __name__ == "__main__":
    test_path = ""
    build_dataframe(test_path)
