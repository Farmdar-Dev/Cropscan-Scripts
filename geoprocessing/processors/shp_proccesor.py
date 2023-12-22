import geopandas as geopd
import pandas as pd
from processors.dataframe_processor import build_dataframe , reproject_df_crs
from constants.generic import PREDICTED_COLUMN

def process_shapefiles(shapefile_paths, unit):
    """
    Read shapefiles and return a list of GeoDataFrames.
    Args:
    shapefile_paths: A list of paths to shapefiles.
    unit: Unit of area to be used for calculations.
    Returns:
    A list of GeoDataFrames split by crop.
    """
    merged_dataframe = merge_shapefiles(shapefile_paths)

    # crs reprojection TODO: Remove this when CRS is standardized
    reproject_df_crs(merged_dataframe)
    # Splitting merged_df to different dataframes that has seperate crops
    dataframes_by_crop = split_dfs_by_predicted(merged_dataframe)
    return dataframes_by_crop


def merge_shapefiles(shapefile_paths):
    """
    Read shapefiles and return a list of GeoDataFrames.
    Args:
    shapefile_paths: A list of paths to shapefiles.
    unit: Unit of area to be used for calculations.
    Returns:
    A list of GeoDataFrames.
    """
    dataframes = build_dataframe(shapefile_paths)
    merged_dataframe = geopd.GeoDataFrame(
        pd.concat(dataframes, ignore_index=True, copy=False))
    return merged_dataframe



def split_dfs_by_predicted(merged_dataframe):
    """
    Split a list of GeoDataFrames by the value of the 'predicted' column.
    Args:
    dataframes: A list of GeoDataFrames.
    Returns:
    A list of GeoDataFrames.
    """

    # changing datatype of column 'predicted' to integer
    merged_dataframe[PREDICTED_COLUMN] = merged_dataframe[PREDICTED_COLUMN].astype(int)
    unique_crops = merged_dataframe[PREDICTED_COLUMN].unique()

    # Splitting merged_df to different dataframes that has seperate crops
    # TODO: [2] see if this can be standardized
    filtered_dataframes = []

    for crop_id in unique_crops:
        filtered_df = merged_dataframe[merged_dataframe[PREDICTED_COLUMN] == crop_id]
        filtered_dataframes.append(filtered_df)

    return filtered_dataframes


def shp_validator():
    pass


if __name__ == "__main__":
    shapefile_paths = ["../data/shapefiles/1.shp", "../data/shapefiles/2.shp"]
    unit = "km"
    process_shapefiles(shapefile_paths, unit)
