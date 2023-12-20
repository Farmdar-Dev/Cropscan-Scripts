from processors.json_processor import read_config_json
from constants.crop_dict import color_id, crop_name
from processors.shp_proccesor import process_shapefiles
from intersection.intersect import intersect
def run():
    print("Reading data...")

if __name__ == "__main__":
    config = read_config_json("config.json")
    dataframes_by_crop = process_shapefiles(config["shapefile_paths"], config["unit"])
    print(dataframes_by_crop)
    #intersected_dataframes = intersect(dataframes_by_crop, config["boundary_file_path"])
    