import geopandas as geopd
import pandas as pd
from utils.area_calculation import calculate_area


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
    merged_dataframe, og_crs = project_crs(merged_dataframe)

    # Splitting merged_df to different dataframes that has seperate crops
    dataframes_by_crop = split_dfs_by_predicted(merged_dataframe)

    for dataframe in dataframes_by_crop:
        calculate_area(dataframe, unit)
        dataframe.to_crs(og_crs, inplace=True)
        dataframe.reset_index(drop=True, inplace=True)
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
    dataframes = []
    for path in shapefile_paths:
        dataframes.append(geopd.read_file(path))
    merged_dataframe = geopd.GeoDataFrame(
        pd.concat(dataframes, ignore_index=True))
    return merged_dataframe


def project_crs(shapefile):
    """
    Estimate the CRS of a shapefile and reproject it to that CRS.
    Args:
    shapefile: A GeoDataFrame.
    Returns:
    A GeoDataFrame.
    """
    # storing orignal crs of dataframe
    og_crs = shapefile.crs
    # Changing the crs of dataframe to estimate crs
    estimated_utm_crs = shapefile.estimate_utm_crs().to_string()
    shapefile = shapefile.to_crs(estimated_utm_crs)
    return shapefile, og_crs


def split_dfs_by_predicted(merged_dataframe):
    """
    Split a list of GeoDataFrames by the value of the 'predicted' column.
    Args:
    dataframes: A list of GeoDataFrames.
    Returns:
    A list of GeoDataFrames.
    """

    # TODO: [1] fix this id change

    # changing datatype of column 'predicted' to integer
    merged_dataframe['predicted'] = merged_dataframe['predicted'].astype(int)
    # changing name of column 'predicted' to 'crop id'
    merged_dataframe = merged_dataframe.rename(
        columns={'predicted': 'crop id'})
    # making variable called 'pred_arr' that stores all unique crop id in data
    unique_crops = merged_dataframe['crop id'].unique()

    # Splitting merged_df to different dataframes that has seperate crops
    # TODO: [2] see if this can be standardized
    filtered_dataframes = []

    for crop_id in unique_crops:
        filtered_df = merged_dataframe[merged_dataframe['crop id'] == crop_id]
        filtered_dataframes.append(filtered_df)

    return filtered_dataframes


def shp_validator():
    pass


if __name__ == "__main__":
    shapefile_paths = ["../data/shapefiles/1.shp", "../data/shapefiles/2.shp"]
    unit = "km"
    process_shapefiles(shapefile_paths, unit)
