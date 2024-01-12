import geopandas as geopd
import pandas as pd
from processors.dataframe_processor import build_dataframe , reproject_df_crs, split_dfs_by_predicted, merge_df

def process_shapefiles(shapefile_paths, priority_crs):
    """
    Read shapefiles and returns a single GeoDataFrame with crs.
    Args:
    shapefile_paths: A list of paths to shapefiles.
    A geodataframe.
    """
    merged_dataframe = merge_shapefiles(shapefile_paths, priority_crs)

    # crs reprojection TODO: Remove this when CRS is standardized
    #reproject_df_crs(merged_dataframe)
    
    return merged_dataframe
    


def merge_shapefiles(shapefile_paths, priority_crs):
    """
    Read shapefiles and returns a single GeoDataFrames.
    Args:
    shapefile_paths: A list of paths to shapefiles.
    A list of GeoDataFrames.
    """
    dataframes = build_dataframe(shapefile_paths)
    
    # reprojection must happen before appending dfs
    shapefiles_reproj = []
    
    for shapefile in dataframes:
        shapefile = shapefile.to_crs(priority_crs)
        shapefiles_reproj.append(shapefile)
    
    merged_dataframe = merge_df(shapefiles_reproj)
    return merged_dataframe


def shp_validator():
    pass


if __name__ == "__main__":
    shapefile_paths = ["../data/shapefiles/1.shp", "../data/shapefiles/2.shp"]
    unit = "km"
    process_shapefiles(shapefile_paths, unit)
