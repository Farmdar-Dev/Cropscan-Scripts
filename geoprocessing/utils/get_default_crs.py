
import geopandas as gpd




def get_crs_string(file_path):
    gdf = gpd.read_file(file_path)
    utm_crs = gdf.estimate_utm_crs()
    if utm_crs:
        zone_number = int(utm_crs.srs.split('UTM zone ')[1][:2])
        if 41 <= zone_number <= 43:
            return "EPSG:32642"
        else:
            return utm_crs.to_string()
    return "CRS could not be estimated"