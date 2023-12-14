import os
import pandas as pd
import geopandas as gp
from dict import color_id, crop_name, variant_name, other_status
import json

# Retrieve JSON data from the file
with open("input.json", "r") as file:
    input = json.load(file)

# Access and process the retrieved JSON data
report_type = input["report_type"]
file_path = input["file_path"]
unit = input["unit"]
df = gp.read_file(file_path)
og_crs = df.crs


def calculate_area(unit, df):
    if unit == 'acres':
        df['Area Acres'] =  (df.area / 4046.8564224).round(2)
    if unit == 'hectares':
        df['Area Hectares'] =  (df.area / 10000).round(2)
        
estimated_utm_crs = df.estimate_utm_crs().to_string()
df = df.to_crs(estimated_utm_crs)
calculate_area(unit, df)
df = df.to_crs(og_crs)
df['predicted'] = df['predicted'].astype(int)


if report_type == 'L1':
    crop_ids = df['predicted'].unique()
    i = 0
    while i < len(crop_ids):
        unique_df = df[df['predicted'] == crop_ids[i]]
        unique_df.insert(0, 'id', range(1, 1 + len(unique_df)))
        unique_df = unique_df.drop('predicted', axis=1)
        name = crop_name[crop_ids[i]]
        path = os.path.dirname(file_path)
        unique_df.to_file(f"{path}/{name}.geojson", driver = 'GeoJSON')
        i = i + 1
        
elif report_type == 'L3':
    df['Variety'] = df['predicted'].apply(lambda x : variant_name[x])
    df['c_id'] = df['predicted'].apply(lambda x : color_id[x])
    df = df.drop('predicted', axis=1)
    df.insert(0, 'id', range(1, 1 + len(df)))
    path = os.path.dirname(file_path)
    df.to_file(f"{path}/varieties.geojson", driver = 'GeoJSON')
    
else:
    df['Class'] = df['predicted'].apply(lambda x : other_status[x])
    df = df.drop('predicted', axis=1)
    df.insert(0, 'id', range(1, 1 + len(df)))
    path = os.path.dirname(file_path)
    df.to_file(f"{path}/{report_type}.geojson", driver = 'GeoJSON')
