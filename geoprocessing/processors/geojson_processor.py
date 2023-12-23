from constants.crop_dict import crop_dictionary 
 
 
def to_geojson(df, path, crop_id):
    """
    Saves report(s) as geojson
    Args:
    df: A dataframe
    path: path to save geojson to
    crop_type: name of file as crop name, report name, etc.    
    """
    name = crop_dictionary[crop_id]
    df.to_file(f"{path}/{name}.geojson", driver = 'GeoJSON')
    