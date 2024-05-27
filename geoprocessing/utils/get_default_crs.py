import geopandas as gpd
from pyproj import CRS

def get_crs_string(file_path):
    gdf = gpd.read_file(file_path)
    utm_crs = gdf.estimate_utm_crs()
    if utm_crs:
        crs_str = utm_crs.to_string()
        if any(zone in crs_str for zone in ['EPSG:32641', 'EPSG:32642', 'EPSG:32643']):
            return CRS.from_epsg("32642")
        else:
            return crs_str
    return "CRS could not be estimated"