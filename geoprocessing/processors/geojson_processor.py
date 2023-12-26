from constants.crop_dict import crop_dictionary 
import os
 
 
def to_geojson(df, path, name):
    """
    Saves report(s) as geojson
    Args:
    df: A dataframe
    path: path to save geojson to
    crop_type: name of file (eg: sugarcane, Variety Scan, Nitrogen report etc.)    
    """
    path = path + "/Tilesets"

    try:
        os.mkdir(path)
    except FileExistsError:
        pass  
    except Exception as e:
        print(f"An error occurred while trying to create the output folder: {e}")
    
    df.to_file(f"{path}/{name}.geojson", driver = 'GeoJSON')
    