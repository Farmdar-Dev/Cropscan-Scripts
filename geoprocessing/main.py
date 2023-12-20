from processors.json_processor import read_config_json
#from constants.crop_dict import color_id, crop_name
from processors.shp_proccesor import process_shapefiles
from intersection.intersect import intersect_caller
def run():
    print("Reading data...")



if __name__ == "__main__":
    config = read_config_json("config.json")
    dataframes_by_crop = process_shapefiles(config["shapefile_paths"], config["unit"])
    #intersected_dataframes = intersect_caller(dataframes_by_crop, config["boundary_file_paths"])
    for dataframe in dataframes_by_crop:
        interesected_df = intersect_caller(dataframe, config["boundary_file_paths"])
        print( "INTERSECTED DATAFRAME")
        print(interesected_df)