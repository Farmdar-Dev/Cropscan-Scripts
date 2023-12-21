import geopandas as gpd



def build_dataframe(filepaths: list):
    """
    Converts file paths into dataframes

    Args:
        filepaths (list): _description_
    """
    dataframes = [gpd.read_file(file) for file in filepaths]


def validate_dataframe():
    pass


if __name__ == "__main__":
    test_path = ""
    build_dataframe(test_path)
