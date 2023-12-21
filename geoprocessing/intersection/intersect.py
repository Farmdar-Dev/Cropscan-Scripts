import geopandas as gpd
import pandas as pd
import os
from constants.crop_dict import crop_dictionary
from utils.area_calculation import calculate_area
from constants.generic import PREDICTED_COLUMN
from processors.dataframe_processor import reproject_dfs_crs
# TODO: use function in dataframe processor all across the code for reprojection



def intersect_all(crop_dfs, boundary_file_paths, output_folder, unit, survey_titles):
    """
    Intersects each crop dataframe with each boundary dataframe and aggregates the results.
    """
    boundary_dfs = [gpd.read_file(path) for path in boundary_file_paths]
    # Have to store original geometry because the dataframe is converted to UTM CRS - it messed up geometries
    # and overlay() doesn't work with different CRS
    # As a workaround, we'll restore the original geometry before any operation and replace based on the id column
    # Also since boundary_dfs is a list of dataframes, I have added unique identifier to each dataframe for conflict resolution
    for idx, boundary_df in enumerate(boundary_dfs):
        boundary_df['original_geometry'] = boundary_df.geometry
        boundary_df['boundary_id'] = idx  # Unique identifier for each boundary

    reproject_dfs_crs(boundary_dfs)
    reproject_dfs_crs(crop_dfs)

    crop_names = [crop_dictionary.get(
        df[PREDICTED_COLUMN].iloc[0], 'Unknown Crop') for df in crop_dfs]

    all_intersections = []
    for boundary_df in boundary_dfs:
        for crop_df, crop_name in zip(crop_dfs, crop_names):
            intersection = gpd.overlay(
                crop_df, boundary_df, how='intersection')
            intersection['crop'] = crop_name
            all_intersections.append(intersection)

    aggregated_data = aggregate_intersections(all_intersections, unit)
    pivoted_data = pivot_data(aggregated_data)
    save_combined_as_geojson(pivoted_data, boundary_dfs, output_folder, survey_titles)


def aggregate_intersections(intersections, unit):
    """
    Aggregates intersection data to calculate the total acreage of each crop in each polygon.
    Uses the unique boundary identifier for accurate aggregation.
    """
    aggregated_data = pd.concat(intersections)
    aggregated_data['acreage'] = calculate_area(aggregated_data, unit)
    return aggregated_data.groupby(['boundary_id', 'id', 'crop'])['acreage'].sum().reset_index()


def pivot_data(df):
    """
    Pivot the data to have crops as columns and their acreage as values.
    """
    pivot_df = df.pivot(index=['boundary_id', 'id'],
                        columns='crop', values='acreage').reset_index()
    return pivot_df.fillna(0)  # Fill NaNs with 0


def save_combined_as_geojson(df, boundary_dfs, output_folder, survey_titles):
    """
    Saves the pivoted data as a single combined GeoJSON file.
    Restores the original geometry before saving.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for idx, boundary_df in enumerate(boundary_dfs):
        output_path = os.path.join(output_folder, f'${survey_titles[idx]}.geojson')
        combined_df = boundary_df.merge(df, on=['boundary_id', 'id'])
        combined_df.geometry = combined_df['original_geometry']
        combined_df.drop(columns=['original_geometry',
                         "boundary_id"], inplace=True)
        combined_df.to_file(output_path, driver='GeoJSON')
