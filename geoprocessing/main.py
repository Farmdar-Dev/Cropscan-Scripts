from processors.json_processor import read_config_json , survey_json_creator
# from constants.crop_dict import color_id, crop_name
from processors.shp_proccesor import process_shapefiles
from intersection.intersect import intersect_all


def run():
    print("Reading data...")


if __name__ == "__main__":
    config = read_config_json("config.json")
    unit = config["unit"]
    dataframes_by_crop = process_shapefiles(config["shapefile_paths"], unit)
    intersected_dataframes = intersect_all(
        dataframes_by_crop, config["boundary_details"], "output", unit, config["esurvey_path"])
    for df in intersected_dataframes:
        print(df)
    survey_json_creator(intersected_dataframes, config)
