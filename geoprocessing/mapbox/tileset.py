
from processors.dataframe_processor import assign_class, assign_color_id, delete_predictions, add_index, merge_df
from processors.geojson_processor import to_geojson
import pandas as pd
import geopandas as gp
import json
from constants.generic import PREDICTED_COLUMN
from utils.area_calculation import calculate_area
from constants.crop_dict import crop_dictionary




def create_tilesets(df_list, config):
    """
    Creates tilesets for the shapefiles user sent as input. To be uploaded to mapbox
    
    Args: 
    df_list: Dataframes list divided by prediction number.  
    config: details from config.json file
    """
    if config["report_type"] == "Crop Scan":
       return L1_tilesets(df_list, config)
    other_tilesets(df_list, config)    

def L1_tilesets(df_list, config):
    """
    Caters to creating tiles for L1 (Crop Scan)
    
    Args: 
    df_list: Dataframes list divided by prediction number. 
    config: details from config.json file   
    """
    for crop_df in df_list:
        crop_df = add_index(crop_df)
        crop_df["area"] = calculate_area(crop_df, config["unit"])
        id = crop_df[PREDICTED_COLUMN].iloc[0]
        crop_name = crop_dictionary[id]
        crop_df = delete_predictions(crop_df)
        to_geojson(crop_df, config['save_path'], crop_name)  
        
            
def other_tilesets(df_list, config):
    """
    Caters to creating tiles for reports other than L1 (L3 etc.)
    
    Args: 
    df_list: Dataframes list divided by prediction number.  
    config: details from config.json file   
    """
    one_df = merge_df(df_list)
    one_df  = assign_class(one_df)
    one_df = assign_color_id(one_df)
    one_df = delete_predictions(one_df)
    one_df = add_index(one_df)
    one_df["area"] = calculate_area(one_df, config["unit"])
    to_geojson(one_df, config['save_path'], config['report_type'])


            
    # case _ :
    #     pass        


# if __name__ == "__main__":
#     smoke_test()
    
