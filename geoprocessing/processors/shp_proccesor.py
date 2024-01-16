import geopandas as geopd
import pandas as pd
from processors.dataframe_processor import build_dataframe , reproject_df_crs, split_dfs_by_predicted, merge_df
from shapely.validation import make_valid
from constants.generic import DEFAULT_CRS
def process_shapefiles(shapefile_paths):
    """
    Read shapefiles and returns a single GeoDataFrame with crs.
    Args:
    shapefile_paths: A list of paths to shapefiles.
    A geodataframe.
    """
    
    print("processing shapefiles")
    merged_dataframe = merge_shapefiles(shapefile_paths, DEFAULT_CRS)
    merged_dataframe.geometry = merged_dataframe.geometry.apply(lambda geom: fix_invalid_geometry(geom))
    merged_dataframe = explode_df(merged_dataframe)
    merged_dataframe = explode_df(merged_dataframe)
    merged_dataframe = extract_polygons(merged_dataframe)
    print("shapefiles processed")
    return merged_dataframe

def extract_polygons(df):
    rows_to_drop = []
    final_df = []

    for index, row in df.iterrows():
        if row['geometry'].geom_type != 'Polygon':
            rows_to_drop.append(index)
        elif row['geometry'].geom_type == 'MultiPolygon':
            print("multi polygon found")
    df = df.drop(rows_to_drop, axis=0)
    df = df.reset_index(drop=True)
    final_df.append(df)
    concat_df = pd.concat(final_df)
    
    return concat_df
        

def explode_df(df):
    df = df.explode(column=None, ignore_index=True)
    return df

def fix_invalid_geometry(geometry):
    if geometry is None:
        print("some row in shapefile has no")
        return 
    if not geometry.is_valid:
        return make_valid(geometry)
    else:
        return geometry

def drop_duplicates(df):
    df = df.drop_duplicates(ignore_index=True)
    return df

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
