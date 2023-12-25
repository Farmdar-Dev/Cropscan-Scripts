# import libraries and functions
from processors.shp_proccesor import process_shapefiles
from processors.json_processor import read_config_json
from processors.dataframe_processor import assign_class, assign_color_id, delete_predictions, add_index, split_dfs_by_predicted
from processors.geojson_processor import to_geojson
import pandas as pd
import geopandas as gp
import json
from constants.generic import PREDICTED_COLUMN
from utils.area_calculation import calculate_area


# def smoke_test():
#     print("Smoke test passed!")
    

# Retrieve JSON data from the file
input = read_config_json("config.json")
report_type = input['report_type']

# Access and process the retrieved JSON data

# turn shapefile(s) into 1 dataframe
one_df = process_shapefiles(input["shapefile_paths"])


match input['is_L1']:
    
    case False:
        assign_class(one_df)
        assign_color_id(one_df)
        delete_predictions(one_df)
        add_index(one_df)
        calculate_area(one_df, input["area_unit"])
        to_geojson(one_df, input['save_path'], report_type)

    case True:
        df_list = split_dfs_by_predicted(one_df)
        for i in df_list:
            add_index(i)
            calculate_area(i, input["area_unit"])
            id = i[PREDICTED_COLUMN].iloc[0]
            delete_predictions(i)
            to_geojson(i, input['save_path'], id)
            
    # case _ :
    #     pass        


# if __name__ == "__main__":
#     smoke_test()
    
