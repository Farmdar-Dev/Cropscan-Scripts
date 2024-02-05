#importing libraries

import geopandas as gpd
import json
import fiona
from processors.json_processor import read_config_json
from processors.dataframe_processor import to_tuple
from processors.shp_proccesor import fix_invalid_geometry, explode_df, extract_polygons
import geopandas as gpd
from utils.area_calculation import calculate_area
from processors.geojson_processor import to_geojson
import pandas as pd
import time




def intersect(overlap, boundaries_tuple, config):
    
    stats = []
    
    print("Generating stats...")
    for title, boundary_df in boundaries_tuple:
        containment = gpd.overlay(boundary_df, overlap, keep_geom_type=True, make_valid=True)
        containment['area'] = calculate_area(containment, config['unit'])
        con_grouped = containment.groupby(['Boundary Name', 'id', 'title'])['area'].sum().reset_index()
        stats.append(con_grouped)
    
    print("Saving stats...")
    pd.concat(stats).to_csv(config['output_path'] + '/stats.csv')
        
    

def run():
    
    print("Reading data...")
    config = read_config_json("overlap/config.json")
    
    boundaries_tuples = to_tuple(config["boundaries"])
    shapefiles_tuples = to_tuple(config["shapefiles"])
    
    print("Preprocessing data...")
    
    for title, boundary_df in boundaries_tuples:
        boundary_df['title'] = title
    
    for title, shapefile_df in shapefiles_tuples:
        shapefile_df.geometry = shapefile_df.geometry.apply(lambda geom: fix_invalid_geometry(geom))
        
    shapefiles = []
        
    for title, shapefile_df in shapefiles_tuples:
        shapefile_df = explode_df(shapefile_df)
        shapefile_df = explode_df(shapefile_df)
        shapefile_df = extract_polygons(shapefile_df)
        shapefile_df = shapefile_df.drop('original_geometry', axis='columns')
        shapefiles.append(shapefile_df)
    
    print("Finding overlapping area...")
    overlap = gpd.overlay(shapefiles[0], shapefiles[1], keep_geom_type=True, make_valid=True)
    
    print("Preparing tile...")
    overlap.geometry = overlap.geometry.apply(lambda geom: fix_invalid_geometry(geom))
    overlap = explode_df(overlap)   
    overlap = explode_df(overlap)
    overlap = extract_polygons(overlap) 
    overlap = overlap.rename(columns ={'predicted_1':shapefiles_tuples[0][0], 'predicted_2':shapefiles_tuples[1][0]})
    
    print("Calculating area..")
    overlap['area'] = calculate_area(overlap, config['unit'])
    overlap = extract_polygons(overlap)
    
    print("Saving tile...")
    to_geojson(overlap, config['output_path'], 'overlap')
    
    intersect(overlap, boundaries_tuples, config)
    

if __name__ == "__main__":
    start = time.time()
    run()    
    end = time.time()
    print("Time taken:", (end - start) / 60)
    
    
    