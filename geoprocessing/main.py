import copy
import os
import time
import multiprocessing
from dotenv import load_dotenv
from multiprocessing import Queue
from processors.json_processor import read_config_json, survey_json_creator
from processors.shp_proccesor import process_shapefiles
from intersection.intersect import intersect_all
from processors.dataframe_processor import split_dfs_by_predicted
from mapbox.tileset import create_tilesets
from awsmodule.s3_download import download_shp_file, download_boundaries, download_esurvey

def run_create_tilesets(dataframes, config, error_queue):
    try:
        create_tilesets(dataframes, config)
    except Exception as e:
        error_queue.put(str(e))


def run():
    print("Reading data...")
    try:
        load_dotenv()
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        bucket = os.getenv("bucket")
        config = read_config_json("D:/farmdar/dashboard/tileset/Cropscan-Scripts/config.json")
        print("Downloading shapefile...")
        shape_file_path = download_shp_file(bucket, config["save_path"], config["shp_name_s3"], aws_access_key_id, aws_secret_access_key)
        shapefiles = process_shapefiles(shape_file_path)
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
        print("Downloading boundaries...")
        
        boundary_dict = download_boundaries(bucket, config["save_path"], config["boundary_details"], aws_access_key_id, aws_secret_access_key)
        if config["esurvey_path"] == "":
            esurvey_path = ""
        else:
            print("Downloading esurvey...")
            esurvey_path = download_esurvey(bucket, config["save_path"], config["esurvey_path"], aws_access_key_id, aws_secret_access_key)
        print("Creating survey JSON...")
        intersected_dataframes = intersect_all(
            dataframes_by_crop, boundary_dict, "output", config["unit"], esurvey_path)
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
