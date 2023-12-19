import pandas as pd
import geopandas as gp
import json
from shapely.geometry import Point
from json_parser import read_config
from constants.crop_dict import color_id, crop_name
def run():
    print("Reading data...")

if __name__ == "__main__":
    config = read_config("config.json")
    print(config)
    print(color_id)