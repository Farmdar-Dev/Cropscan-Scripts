from constants.crop_dict import crop_dictionary 
from constants.generic import TARGET_CRS
import os
 
 
def to_geojson(df, path, name):
    """
    Saves report(s) as geojson
    Args:
    df: A dataframe
    path: path to save geojson to
    crop_type: name of file (eg: sugarcane, Variety Scan, Nitrogen report etc.)    
    """
    path = os.path.join(path, "Tilesets")

    
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except Exception as e:
            print(f"An error occurred while trying to create the output folder: {e}")
            return

    df = df.to_crs(TARGET_CRS)
    df.to_file(f"{os.path.join(path, name)}.geojson", driver='GeoJSON')