import geopandas as geopd
import pandas as pd
from area_calculation import calculate_area


def process_shapefiles(shapefile_paths, unit):
    merged_dataframe = merge_shapefiles(shapefile_paths)
    
    #crs reprojection TODO: Remove this when CRS is standardized
    merged_dataframe, og_crs = project_crs(merged_dataframe)


    # changing datatype of column 'predicted' to integer
    merged_dataframe['predicted'] = merged_dataframe['predicted'].astype(int)
    # changing name of column 'predicted' to 'crop id'
    merged_dataframe = merged_dataframe.rename(columns = {'predicted': 'crop id'})
    # making variable called 'pred_arr' that stores all unique crop id in data
    pred_arr = merged_dataframe['crop id'].unique()
    
    # Splitting merged_df to different dataframes that has seperate crops and storing them in array "dfs_out"
    dfs_out = []
    
    for i in pred_arr:
        dfs_out.append(merged_dataframe[merged_dataframe['crop id'] == i]) 
        
    # For each dataframe in dfs_out

    for i in range(len(dfs_out)):
        #Adding area column
        calculate_area(dfs_out[i], unit)

       # Changing crs back to orignal crs    
        dfs_out[i] = dfs_out[i].to_crs(og_crs)
        
        # reseting index of all dataframes

        dfs_out[i] = dfs_out[i].reset_index(drop=True)
        
    return dfs_out


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
    merged_dataframe = geopd.GeoDataFrame(pd.concat(dataframes, ignore_index=True))
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


def split_dfs_by_predicted(dataframes):
    """
    Split a list of GeoDataFrames by the value of the 'predicted' column.
    Args:
    dataframes: A list of GeoDataFrames.
    Returns:
    A list of GeoDataFrames.
    """
    dfs_out = []
    for df in dataframes:
        predicted_values = df['predicted'].unique()
        for value in predicted_values:
            dfs_out.append(df[df['predicted'] == value])
    return dfs_out




if __name__ == "__main__":
    shapefile_paths = ["../data/shapefiles/1.shp", "../data/shapefiles/2.shp"]
    unit = "km"
    process_shapefiles(shapefile_paths, unit)