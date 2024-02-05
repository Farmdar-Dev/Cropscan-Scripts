import geopandas as gpd

def get_crs_string(file_path):
    gdf = gpd.read_file(file_path)
    utm_crs = gdf.estimate_utm_crs()
    if utm_crs:
        crs_str = utm_crs.to_string()
        if any(zone in crs_str for zone in ['UTM zone 41', 'UTM zone 42', 'UTM zone 43']):
            return "EPSG:32642"
        else:
            return crs_str
    return "CRS could not be estimated"