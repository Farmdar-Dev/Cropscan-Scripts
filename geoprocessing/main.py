import copy
import time
import multiprocessing
from processors.json_processor import read_config_json, survey_json_creator
from processors.shp_proccesor import process_shapefiles
from intersection.intersect import intersect_all
from processors.dataframe_processor import split_dfs_by_predicted
from mapbox.tileset import create_tilesets 

def run_create_tilesets(dataframes, config):
    create_tilesets(dataframes, config)

def run():
    print("Reading data...")
    config = read_config_json("config.json")
    shapefiles = process_shapefiles(config["shapefile_paths"])
    dataframes_by_crop = split_dfs_by_predicted(shapefiles)
    deep_copied_dataframes = [copy.deepcopy(df) for df in dataframes_by_crop]

    print("Creating tilesets...")
    tileset_process = multiprocessing.Process(target=run_create_tilesets, args=(deep_copied_dataframes, config))
    tileset_process.start()
    print("Creating survey JSON...")
    intersected_dataframes = intersect_all(
        dataframes_by_crop, config["boundary_details"], "output", config["unit"], config["esurvey_path"])
    survey_json_creator(intersected_dataframes, config)

    tileset_process.join()  # Wait for the tileset process to finish
    end = time.time()
    print("Time taken:", (end - start) / 60)

if __name__ == "__main__":
    start = time.time()
    run()
