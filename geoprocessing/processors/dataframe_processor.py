import geopandas as gpd
import pandas as pd
from constants.generic import PREDICTED_COLUMN
from utils.area_calculation import calculate_area
from constants.crop_dict import crop_dictionary
from constants.color_dict import color_id
from utils.get_default_crs import get_gdf_crs_string


def to_tuple(boundary_dict, crs_string):
    # Create tuples of (title, dataframe)
    boundary_tuples = [(title, gpd.read_file(path))
    for title, path in boundary_dict.items()]


    print("Reprojecting boundaries.")
    # Reproject CRS if necessary and other preprocessing
    for title, boundary_df in boundary_tuples:
        boundary_df['original_geometry'] = boundary_df.geometry
        boundary_df['layer_id'] = id(boundary_df)
        boundary_df.to_crs(crs_string, inplace = True)
        
    print("Preprocessing boundaries.")
    boundary_tuples = drop_duplicates_tuple(boundary_tuples)
    
    print("Preprocessing complete.")
    return boundary_tuples 

def drop_duplicates_tuple(df_tuple):

    df_tuple_simplified = []

    for title, df in df_tuple:
        df = df.drop_duplicates(ignore_index=True)
        # df_tuple_simplified.append([(title, df)])
        df_tuple_simplified.append((title, df))
    return df_tuple_simplified  

def build_dataframe(filepaths: list):
    """
    Converts file paths into dataframes

    Args:
        filepaths (list): a list of shapefile paths
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
        crs = get_gdf_crs_string(dataframe)
    dataframe.to_crs(crs, inplace=True)


def reproject_dfs_crs(dataframes: list, crs=None):
    """
    Reprojects the list of dataframe to the specified CRS
    if no CRS is specified, it will estimate the utm CRS
    """
    [reproject_df_crs(df, crs) for df in dataframes]
    

def split_dfs_by_predicted(merged_dataframe):
    """
    Split a GeoDataFrames by the value of the 'predicted' column.
    Args:
    dataframes: A list of GeoDataFrames.
    Returns:
    A list of GeoDataFrames.i
    """

    # changing datatype of column 'predicted' to integer
    merged_dataframe[PREDICTED_COLUMN] = merged_dataframe[PREDICTED_COLUMN].astype(int)
    #gathering unique crop ids
    unique_crops = merged_dataframe[PREDICTED_COLUMN].unique()

    # Splitting merged_df to different dataframes that has seperate crops
    # TODO: [2] see if this can be standardized
    filtered_dataframes = []

    for crop_id in unique_crops:
        filtered_df = merged_dataframe[merged_dataframe[PREDICTED_COLUMN] == crop_id].copy()
        filtered_dataframes.append(filtered_df)

    return filtered_dataframes


def assign_class(df):
    """
    Adds 'class' column to dataframe
    Args:
    df: A dataframe
    Returns:
    manipulated column
    """
    df[PREDICTED_COLUMN] = df[PREDICTED_COLUMN].astype(int)
    df['Class'] = df[PREDICTED_COLUMN].apply(lambda x : crop_dictionary[x])
    return df
    
def assign_color_id(df):
    """
    Adds 'c_id' (color id) column to dataframe
    Args:
    df: A dataframe
    Returns:
    manipulated column
    """
    df[PREDICTED_COLUMN] = df[PREDICTED_COLUMN].astype(int)
    df['c_id'] = df[PREDICTED_COLUMN].apply(lambda x : color_id[int(x)])
    return df
    
def delete_predictions(df):
    """
    Deletes the prediction column from a dataframe
    Args:
    df: A dataframe
    Returns:
    manipulated dataframe
    """
    del df[PREDICTED_COLUMN]
    return df
    
def add_index(df):
    """
    Adds an index column by the name of 'id' to dataframe
    Args:
    df: A dataframe
    Returns:
    manipulated dataframe
    """
    df.insert(0, 'id', range(1, 1 + len(df)))
    return df
    
def merge_df(list_of_df):
    """
    Merges a list of df into one df
    Args: a list of dataframes
    returns: one single dataframe
    """
    merged = pd.concat(list_of_df)
    return merged


if __name__ == "__main__":
    test_path = ""
    build_dataframe(test_path)
