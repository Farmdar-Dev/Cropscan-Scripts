import copy
from processors.json_processor import read_config_json , survey_json_creator
# from constants.crop_dict import color_id, crop_name
from processors.shp_proccesor import process_shapefiles
from intersection.intersect import intersect_all
from processors.dataframe_processor import split_dfs_by_predicted
from tilesets import create_tilesets
import time 
def run():
    print("Reading data...")


if __name__ == "__main__":
    start = time.time()
    config = read_config_json("config.json")
    unit = config["unit"]
    shapefiles = process_shapefiles(config["shapefile_paths"])
    dataframes_by_crop = split_dfs_by_predicted(shapefiles)
    deep_copied_dataframes = [copy.deepcopy(df) for df in dataframes_by_crop]
    create_tilesets(deep_copied_dataframes, config)
    intersected_dataframes = intersect_all(
        dataframes_by_crop, config["boundary_details"], "output", unit, config["esurvey_path"])
    for df in intersected_dataframes:
        print(df)
    print(intersected_dataframes)
    survey_json_creator(intersected_dataframes, config)
    end = time.time()
    print("Time taken:", (end - start)/60)
    
    
