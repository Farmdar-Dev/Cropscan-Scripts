import copy
import os
import time
import multiprocessing
from multiprocessing import Queue
from processors.json_processor import read_config_json, survey_json_creator
from processors.shp_proccesor import process_shapefiles
from intersection.intersect import intersect_all
from processors.dataframe_processor import split_dfs_by_predicted, to_tuple
from mapbox.tileset import create_tilesets


def run_create_tilesets(dataframes, config, error_queue):
    try:
        create_tilesets(dataframes, config)
    except Exception as e:
        error_queue.put(str(e))

def run():
    print("Reading data...")
    config = read_config_json("config.json")
    boundaries_tuples = to_tuple(config["boundary_details"])
    shapefiles = process_shapefiles(config["shapefile_paths"])
    dataframes_by_crop = split_dfs_by_predicted(shapefiles)
    deep_copied_dataframes = [copy.deepcopy(
        df) for df in dataframes_by_crop]
    print("Dataframes seperated moving onto json")
    
    os.makedirs(os.path.join(
        config["save_path"], "Tilesets"), exist_ok=True)
    os.makedirs(os.path.join(config["save_path"], "Json"), exist_ok=True)
    print("Creating tilesets...")

    error_queue = Queue()
    tileset_process = multiprocessing.Process(
        target=run_create_tilesets, args=(deep_copied_dataframes, config, error_queue))
    tileset_process.start()
    print("type of boundary tuples",type( boundaries_tuples))

    print(boundaries_tuples)

    print("Creating survey JSON...")
    intersected_dataframes = intersect_all(
        dataframes_by_crop, boundaries_tuples, config["save_path"], config["unit"], config["esurvey_path"])
    survey_json_creator(intersected_dataframes, config)

    tileset_process.join()

    if not error_queue.empty():
        error_message = error_queue.get()
        print(f"Error in subprocess: {error_message}")

    end = time.time()
    print("Time taken:", (end - start) / 60)



if __name__ == "__main__":
    start = time.time()
    run()
