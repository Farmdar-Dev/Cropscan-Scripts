from constants.crop_dict import crop_dictionary 
from constants.generic import TARGET_CRS
import os
from awsmodule.s3_upload import upload_files

 
def to_geojson(df, path, name, s3_path):
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
    full_path = f"{os.path.join(path, name)}.geojson"
    df.to_file(full_path, driver='GeoJSON')
    s3_path = upload_files(s3_path, full_path, "Tileset")
    