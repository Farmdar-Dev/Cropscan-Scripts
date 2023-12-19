import pandas as pd
import geopandas as gp
import json
from shapely.geometry import Point
from processors.json_processor import read_config_json
from constants.crop_dict import color_id, crop_name
def run():
    print("Reading data...")

if __name__ == "__main__":
    config = read_config_json("config.json")
    print(config)
    print(color_id)