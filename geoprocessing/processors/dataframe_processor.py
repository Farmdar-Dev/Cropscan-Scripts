import geopandas as gpd
import pandas as pd
from constants.generic import PREDICTED_COLUMN
from utils.area_calculation import calculate_area
from constants.crop_dict import crop_dictionary
from constants.color_dict import color_id




def to_tuple(boundary_dict):
    # Create tuples of (title, dataframe)
    boundary_tuples = [(title, gpd.read_file(path))
    for title, path in boundary_dict.items()]
    
    # Reproject CRS if necessary and other preprocessing
    for title, boundary_df in boundary_tuples:
        boundary_df['original_geometry'] = boundary_df.geometry
        boundary_df['layer_id'] = id(boundary_df)
        
    priority_crs = 'WGS 84 / UTM zone 42N'

    for title, boundary_df in boundary_tuples:
        boundary_df = boundary_df.to_crs(boundary_df.estimate_utm_crs())
        
        if boundary_df.crs.name != priority_crs:
            priority_crs = boundary_df.crs
            break

    if priority_crs != 'WGS 84 / UTM zone 42N':
        for title, boundary_df in boundary_tuples:
            boundary_df = boundary_df.to_crs(priority_crs)
    
    return boundary_tuples, priority_crs 
    #the priority crs should ideally pass onto the reprojection function 
    #and be stored there rather than be sent to main


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
        crs = dataframe.estimate_utm_crs()
    dataframe.to_crs(crs, inplace=True)
    pass


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
    
def assign_color_id(df):
    """
    Adds 'c_id' (color id) column to dataframe
    Args:
    df: A dataframe
    Returns:
    manipulated column
    """
    df[PREDICTED_COLUMN] = df[PREDICTED_COLUMN].astype(int)
    df['c_id'] = df[PREDICTED_COLUMN].apply(lambda x : color_id[x])
    
def delete_predictions(df):
    """
    Deletes the prediction column from a dataframe
    Args:
    df: A dataframe
    Returns:
    manipulated dataframe
    """
    del df[PREDICTED_COLUMN]
    
def add_index(df):
    """
    Adds an index column by the name of 'id' to dataframe
    Args:
    df: A dataframe
    Returns:
    manipulated dataframe
    """
    df.insert(0, 'id', range(1, 1 + len(df)))
    
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
