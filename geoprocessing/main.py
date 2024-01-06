import copy
import os
import time
import multiprocessing
from multiprocessing import Queue
from processors.json_processor import read_config_json, survey_json_creator
from processors.shp_proccesor import process_shapefiles
from intersection.intersect import intersect_all
from processors.dataframe_processor import split_dfs_by_predicted
from mapbox.tileset import create_tilesets


def run_create_tilesets(dataframes, config, error_queue):
    try:
        create_tilesets(dataframes, config)
    except Exception as e:
        error_queue.put(str(e))


def run():
    print("Reading data...")
    try:
        config = read_config_json("config.json")
        shapefiles = process_shapefiles(config["shapefile_paths"])
        dataframes_by_crop = split_dfs_by_predicted(shapefiles)
        deep_copied_dataframes = [copy.deepcopy(
            df) for df in dataframes_by_crop]

        
        os.makedirs(os.path.join(
            config["save_path"], "Tilesets"), exist_ok=True)
        os.makedirs(os.path.join(config["save_path"], "Json"), exist_ok=True)
        print("Creating tilesets...")

        error_queue = Queue()
        tileset_process = multiprocessing.Process(
            target=run_create_tilesets, args=(deep_copied_dataframes, config, error_queue))
        tileset_process.start()

        print("Creating survey JSON...")
        intersected_dataframes = intersect_all(
            dataframes_by_crop, config["boundary_details"], "output", config["unit"], config["esurvey_path"])
        survey_json_creator(intersected_dataframes, config)

        tileset_process.join()

        if not error_queue.empty():
            error_message = error_queue.get()
            print(f"Error in subprocess: {error_message}")

        end = time.time()
        print("Time taken:", (end - start) / 60)
    except Exception as e:
        print("An error occurred in the main process: ", e)
        os.rmdir(os.path.join(config["save_path"], "Tilesets"))
        os.rmdir(os.path.join(config["save_path"], "Json"))


if __name__ == "__main__":
    start = time.time()
    run()
