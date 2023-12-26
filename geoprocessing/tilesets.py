# import libraries and functions
#from processors.shp_proccesor import process_shapefiles
#from processors.json_processor import read_config_json
from processors.dataframe_processor import assign_class, assign_color_id, delete_predictions, add_index, merge_df
from processors.geojson_processor import to_geojson
import pandas as pd
import geopandas as gp
import json
from constants.generic import PREDICTED_COLUMN
from utils.area_calculation import calculate_area
from constants.crop_dict import crop_dictionary


# def smoke_test():
#     print("Smoke test passed!")
    

# Retrieve JSON data from the file
#input = read_config_json("config.json")
#we are now getting the config from main.py

# turn shapefile(s) into 1 dataframe
#one_df = process_shapefiles(input["shapefile_paths"])
#we are now getting one_df from the main.py file

def create_tilesets(df_list, config):
    """
    Creates tilesets for the shapefiles user sent as input. To be uploaded to mapbox
    
    Args: 
    df_list: Dataframes list divided by prediction number.  
    config: details from config.json file
    """
    
    match config["is_L1"]:
        case True:
            L1_tilesets(df_list, config)
        case False:
            other_tilesets(df_list, config)
            

def L1_tilesets(df_list, config):
    """
    Caters to creating tiles for L1 (Crop Scan)
    
    Args: 
    df_list: Dataframes list divided by prediction number. 
    config: details from config.json file   
    """
    for crop_df in df_list:
        add_index(crop_df)
        calculate_area(crop_df, config["unit"])
        id = crop_df[PREDICTED_COLUMN].iloc[0]
        crop_name = crop_dictionary[id]
        delete_predictions(crop_df)
        to_geojson(crop_df, config['save_path'], crop_name)  
        
            
def other_tilesets(df_list, config):
    """
    Caters to creating tiles for reports other than L1 (L3 etc.)
    
    Args: 
    df_list: Dataframes list divided by prediction number.  
    config: details from config.json file   
    """
    one_df = merge_df(df_list)
    assign_class(one_df)
    assign_color_id(one_df)
    delete_predictions(one_df)
    add_index(one_df)
    calculate_area(one_df, config["sunit"])
    to_geojson(one_df, config['save_path'], config['report_type'])


            
    # case _ :
    #     pass        


# if __name__ == "__main__":
#     smoke_test()
    
