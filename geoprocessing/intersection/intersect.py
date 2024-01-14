import geopandas as gpd
import pandas as pd
import os
from constants.crop_dict import crop_dictionary
from utils.area_calculation import calculate_area
from constants.generic import PREDICTED_COLUMN, ESURVEY_COLUMN
from processors.dataframe_processor import reproject_dfs_crs, reproject_df_crs
import geopandas as gpd


def add_esurvey_area(boundary_df, esurvey_path, unit):
    """
    Adds the area of the boundary from the e-survey data to the boundary dataframe.
    """
    if esurvey_path == "":
        boundary_df[ESURVEY_COLUMN] = "-"
        return boundary_df

    esurvey_df = gpd.read_file(esurvey_path)
    reproject_df_crs(esurvey_df)
    boundary_df_cpy = boundary_df.copy()
    intersection = gpd.overlay(boundary_df_cpy, esurvey_df, how='intersection')
    intersection[ESURVEY_COLUMN] = calculate_area(intersection, unit)
    intersection = intersection.groupby(['id_1'])[ESURVEY_COLUMN].sum().reset_index()
    intersection = intersection.rename({'id_1': 'id'}, axis='columns')

    boundary_df = boundary_df.merge(
        intersection, on='id', how='left').fillna(0)
    return boundary_df


def intersect_all(crop_dfs, boundary_tuples, output_folder, unit, esurvey_path):
    """
    Intersects each crop dataframe with each boundary dataframe and aggregates the results.
    Utilizes a tuple of (title, dataframe) to maintain the association between the boundary dataframes and their titles.
    """

    # Deriving crop names from the crop dataframes
    crop_names = [crop_dictionary.get(int(df[PREDICTED_COLUMN].iloc[0]), 'Unknown Crop') for df in crop_dfs]

    all_intersections = []
    for title, boundary_df in boundary_tuples:
        for crop_df, crop_name in zip(crop_dfs, crop_names):
            #crop_df["acreage"] = calculate_area(crop_df, unit)
            print("interescting" ,crop_df, "with", boundary_df)
            intersection = gpd.overlay(boundary_df, crop_df, keep_geom_type=True, make_valid=True)
            intersection['crop'] = crop_name
            intersection["acreage"] = calculate_area(intersection, unit)
            _intersection = drop_empty_areas(intersection)
            all_intersections.append(_intersection)
    
    aggregated_data = aggregate_intersections(all_intersections, unit)
    pivoted_data = pivot_data(aggregated_data)

    save_combined_as_geojson(
        pivoted_data, boundary_tuples, output_folder, esurvey_path, unit)

    return make_boundary_aggregated_dfs(pivoted_data, boundary_tuples, esurvey_path, unit)

def drop_empty_areas(df):
    rows_to_drop = []

    for index, row in df.iterrows():
        if row['acreage'] == 0.00:
            rows_to_drop.append(index)
    df = df.drop(rows_to_drop, axis=0)
    df = df.reset_index(drop=True)
    
    return df

def aggregate_intersections(intersections, unit):
    """
    Aggregates intersection data to sum the total acreage of each crop in each polygon.
    Uses the unique boundary identifier for accurate aggregation.
    """
    #[drop_empty_areas(interesction) for interesction in intersections]
    aggregated_data = pd.concat(intersections)
   # aggregated_data['acreage'] = calculate_area(aggregated_data, unit)
    return aggregated_data.groupby(['layer_id', 'id', 'crop'])['acreage'].sum().reset_index()


def pivot_data(df):
    """
    Pivot the data to have crops as columns and their acreage as values.
    """
    pivot_df = df.pivot(index=['layer_id', 'id'],
                        columns='crop', values='acreage').reset_index()
    return pivot_df.fillna(0)  # Fill NaNs with 0


def save_combined_as_geojson(df, boundary_tuples, output_folder, esurvey_df, unit):
    """
    Saves the pivoted data as GeoJSON files, one for each boundary.
    Restores the original geometry before saving and names files based on boundary titles.

    Args:
        df: The dataframe containing the pivoted data.
        boundary_tuples: List of tuples, each containing a title and its corresponding boundary dataframe.
        output_folder: The directory where the GeoJSON files will be saved.
        esurvey_df: DataFrame of the e-survey data.
        unit: Unit for area calculation.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for title, boundary_df in boundary_tuples:
        boundary_df = add_esurvey_area(boundary_df, esurvey_df, unit)
        output_path = os.path.join(output_folder, f'{title}.geojson')
        combined_df = boundary_df.merge(df, on=['layer_id', 'id'])
        combined_df.geometry = combined_df['original_geometry']
        combined_df.drop(
            columns=['original_geometry', "layer_id"], inplace=True)
        combined_df.to_file(output_path, driver='GeoJSON')


def make_boundary_aggregated_dfs(pivoted_data, boundary_tuples, esurvey_df, unit):
    """
    Merges pivoted data with each boundary dataframe and creates a list of aggregated dataframes.
    Now uses tuples of (title, dataframe) for processing.

    Args:
        pivoted_data: The pivoted data containing aggregated crop information.
        boundary_tuples: List of tuples, each containing a title and its corresponding boundary dataframe.
        esurvey_df: DataFrame of the e-survey data.
        unit: Unit for area calculation.
    """
    boundary_wise_dfs = []

    for title, boundary_df in boundary_tuples:
        boundary_df = add_esurvey_area(boundary_df, esurvey_df, unit)
        combined_df = boundary_df.merge(
            pivoted_data, on=['layer_id', 'id'], how='left')
        combined_df.geometry = combined_df['original_geometry']
        combined_df.drop(
            columns=['original_geometry', "layer_id"], inplace=True)
        # Adding title as a column for reference
        combined_df['survey_title'] = title
        boundary_wise_dfs.append(combined_df)

    return boundary_wise_dfs
