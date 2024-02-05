#importing libraries

import geopandas as gpd
import json
import fiona
from processors.json_processor import read_config_json
from processors.dataframe_processor import to_tuple
from processors.shp_proccesor import fix_invalid_geometry, explode_df, extract_polygons
import geopandas as gpd
from utils.area_calculation import calculate_area
import pandas as pd
import time
from overlap.overlap_dict import overlap_dictionary
from constants.generic import TARGET_CRS
import os



def to_shp(df, path, name):
    """
    Saves report(s) as shp
    Args:
    df: A dataframe
    path: path to save shp to
    crop_type: name of file   
    """
    path = os.path.join(path, "Tilesets")

    
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except Exception as e:
            print(f"An error occurred while trying to create the output folder: {e}")
            return

    df = df.to_crs(TARGET_CRS)
    df.to_file(f"{os.path.join(path, name)}.shp")


def intersect(overlap, boundaries_tuple, config):
    """
    Intersects the overlap dataframe with each boundary to generate stats.
    Args:
    overlap: the overlap dataframe.
    boundaries_tuple: tuple containing boundary dataframes
    config: config json data
    Output:
    Generates a stats.csv
    """
    stats = []
    
    print("Generating stats...")
    
    #overlaying overlap tile with each boundary df to generate overlapping area per boundary stats
    
    for title, boundary_df in boundaries_tuple:
        containment = gpd.overlay(boundary_df, overlap, keep_geom_type=True, make_valid=True)
        containment['area'] = calculate_area(containment, config['unit'])
        con_grouped = containment.groupby(['Boundary Name', 'id', 'title'])['area'].sum().reset_index()
        stats.append(con_grouped)
    
    print("Saving stats...")
    pd.concat(stats).to_csv(config['output_path'] + '/stats.csv')
        
    

def run():
    
    """
    Finds overlapping area between two tiles and generates a third.
    """
    
    print("Reading data...")
    config = read_config_json("overlap/config.json")
    
    boundaries_tuples = to_tuple(config["boundaries"])
    shapefiles_tuples = to_tuple(config["shapefiles"])
    
    print("Preprocessing data...")
    
    #adding title column to boundary dataframes
    for title, boundary_df in boundaries_tuples:
        boundary_df['title'] = title
    
    #fixing invalid geom for correct area calculation
    for title, shapefile_df in shapefiles_tuples:
        shapefile_df.geometry = shapefile_df.geometry.apply(lambda geom: fix_invalid_geometry(geom))
        
    shapefiles = []
    
    #reducing shapes to polygons to maintain uniform geometry in dataframes ie. polygon    
    for title, shapefile_df in shapefiles_tuples:
        shapefile_df = explode_df(shapefile_df)
        shapefile_df = explode_df(shapefile_df)
        shapefile_df = extract_polygons(shapefile_df)
        shapefile_df = shapefile_df.drop('original_geometry', axis='columns')
        shapefiles.append(shapefile_df)
    
    print("Finding overlapping area...")
    overlap = gpd.overlay(shapefiles[0], shapefiles[1], keep_geom_type=True, make_valid=True)
    #removing all columns except geometry column
    overlap = overlap[['geometry']]
    
    #repeating preprocessing with new tile created
    print("Preparing tile...")
    overlap.geometry = overlap.geometry.apply(lambda geom: fix_invalid_geometry(geom))
    overlap = explode_df(overlap)   
    overlap = explode_df(overlap)
    overlap = extract_polygons(overlap) 
    #overlap = overlap.rename(columns ={'predicted_1':shapefiles_tuples[0][0], 'predicted_2':shapefiles_tuples[1][0]})
    
    #assigning predicted column
    overlap['predicted'] = overlap_dictionary[config['overlap']]
    
    #area calculation is no longer required
    #overlap['area'] = calculate_area(overlap, config['unit'])
    overlap = extract_polygons(overlap)
    
    print("Saving tile...")
    to_shp(overlap, config['output_path'], config['overlap'])
    
    #the stats.csv generation is no longer required
    #intersect(overlap, boundaries_tuples, config)
    

if __name__ == "__main__":
    start = time.time()
    run()    
    end = time.time()
    print("Time taken:", (end - start) / 60)
    
    
    